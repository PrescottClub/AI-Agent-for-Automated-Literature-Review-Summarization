"""LLM manager for handling OpenAI API interactions."""

import asyncio
from typing import Any, Dict, List, Optional, Literal

import httpx

from ..utils.logger import LoggerMixin, get_logger
from ..utils.config import Config

logger = get_logger(__name__)

# Supported LLM providers
LLMProvider = Literal["openai", "deepseek", "ollama", "mock"]


class LLMManagerError(Exception):
    """Custom exception for LLMManager errors."""

    pass


class LLMManager(LoggerMixin):
    """
    Manages interactions with various Large Language Models (LLMs).
    Handles API calls, error handling, and provider-specific logic.
    """

    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.provider: LLMProvider = self.config.llm_provider
        self.api_key: Optional[str] = None
        self.base_url: Optional[str] = None
        self.model_name: Optional[str] = None
        self.timeout = self.config.llm_timeout_seconds
        self.max_retries = self.config.llm_max_retries

        self._configure_provider()
        self.logger.info(
            f"LLMManager initialized for provider: {self.provider} with model: {self.model_name}"
        )

    def _configure_provider(self):
        """Configures the LLM provider based on the settings."""
        if self.provider == "openai":
            self.api_key = self.config.openai_api_key
            self.base_url = self.config.openai_api_base or "https://api.openai.com/v1"
            self.model_name = self.config.openai_model
            if not self.api_key:
                raise LLMManagerError("OpenAI API key is not configured.")
        elif self.provider == "deepseek":
            self.api_key = self.config.deepseek_api_key
            self.base_url = (
                self.config.deepseek_api_base or "https://api.deepseek.com/v1"
            )
            self.model_name = self.config.deepseek_model
            if not self.api_key:
                raise LLMManagerError("DeepSeek API key is not configured.")
        elif self.provider == "ollama":
            self.base_url = self.config.ollama_api_base or "http://localhost:11434/api"
            self.model_name = self.config.ollama_model
            # Ollama typically doesn't require an API key directly in headers
            self.logger.info(
                f"Ollama provider configured. Ensure Ollama server is running at {self.base_url}"
            )
        elif self.provider == "mock":
            self.logger.info(
                "LLMManager configured with MOCK provider for testing.")
            self.model_name = "mock_model"
        else:
            raise LLMManagerError(f"Unsupported LLM provider: {self.provider}")

    async def _make_request(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        method: str = "POST",
    ) -> Dict[str, Any]:
        """Makes an asynchronous HTTP request to the LLM API."""
        if not self.base_url:
            raise LLMManagerError("LLM base URL is not configured.")

        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = {"Content-Type": "application/json"}
        if (
            self.api_key and self.provider != "ollama"
        ):  # Ollama does not use Bearer token typically
            headers["Authorization"] = f"Bearer {self.api_key}"

        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    self.logger.debug(
                        f"Sending {method} request to {url} with payload: {payload}"
                    )
                    if method == "POST":
                        response = await client.post(url, headers=headers, json=payload)
                    elif method == "GET":
                        response = await client.get(
                            url, headers=headers, params=payload
                        )  # params for GET
                    else:
                        raise LLMManagerError(
                            f"Unsupported HTTP method: {method}")

                    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
                    response_data = response.json()
                    self.logger.debug(
                        f"Received response from {url}: {response_data}")
                    return response_data
            except httpx.HTTPStatusError as e:
                self.logger.error(
                    f"HTTP error {e.response.status_code} for {e.request.url}: {e.response.text}"
                )
                # Unauthorized or Forbidden
                if e.response.status_code in [401, 403]:
                    raise LLMManagerError(
                        f"Authentication error: {e.response.text}"
                    ) from e
                if e.response.status_code == 429:  # Rate limit
                    self.logger.warning(
                        "Rate limit exceeded. Retrying after delay...")
                    await asyncio.sleep(
                        self.config.llm_rate_limit_delay * (attempt + 1)
                    )
                elif attempt == self.max_retries - 1:
                    raise LLMManagerError(
                        f"HTTP error after {self.max_retries} retries: {e}"
                    ) from e
                else:
                    # Basic exponential backoff
                    await asyncio.sleep(1 * (attempt + 1))
            except httpx.RequestError as e:
                self.logger.error(f"Request error for {url}: {e}")
                if attempt == self.max_retries - 1:
                    raise LLMManagerError(
                        f"Request error after {self.max_retries} retries: {e}"
                    ) from e
                await asyncio.sleep(1 * (attempt + 1))
            except Exception as e:
                self.logger.error(
                    f"An unexpected error occurred during LLM request: {e}",
                    exc_info=True,
                )
                raise LLMManagerError(f"Unexpected LLM error: {e}") from e

        raise LLMManagerError(
            f"Failed to get a response from LLM after {self.max_retries} retries."
        )

    async def generate_chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        stream: bool = False,  # Placeholder for future streaming support
    ) -> Dict[str, Any]:  # Adjust return type if streaming is implemented
        """
        Generates a chat completion using the configured LLM provider.

        Args:
            messages: A list of message dictionaries, e.g.,
                      [{"role": "user", "content": "Hello!"}].
            max_tokens: The maximum number of tokens to generate.
            temperature: Sampling temperature.
            stream: Whether to stream the response (not fully implemented for all providers).

        Returns:
            The LLM's response, typically a dictionary containing the completion.
        """
        if self.provider == "mock":
            self.logger.info(
                f"Mocking chat completion for messages: {messages}")
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "This is a mock response.",
                        }
                    }
                ],
                "usage": {"total_tokens": 0},
            }

        if not self.model_name:
            raise LLMManagerError("LLM model name is not configured.")

        payload: Dict[str, Any] = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        # Provider-specific payload adjustments
        endpoint = ""
        if self.provider == "openai" or self.provider == "deepseek":
            endpoint = "chat/completions"
            if stream:
                payload["stream"] = True  # OpenAI/DeepSeek support stream
        elif self.provider == "ollama":
            # Ollama has a slightly different API structure
            endpoint = "chat"
            # Ollama payload needs `model`, `messages`, and `stream` at the top level.
            # It might not support `temperature` or `max_tokens` in the same way directly in /api/chat
            # Often, these are part of the Modelfile or model options when running the model.
            # For simplicity, we pass them, but their effect depends on Ollama setup.
            payload["stream"] = stream
            if "max_tokens" in payload:  # Ollama might use options for this
                payload.setdefault("options", {})["num_predict"] = payload.pop(
                    "max_tokens"
                )
            if "temperature" in payload:
                payload.setdefault("options", {})["temperature"] = payload.pop(
                    "temperature"
                )
        else:
            raise LLMManagerError(
                f"Chat completion not implemented for provider: {self.provider}"
            )

        try:
            response_data = await self._make_request(endpoint, payload)
            # TODO: Standardize response format if providers differ significantly
            # For now, assume OpenAI-like structure for non-streaming
            return response_data
        except LLMManagerError as e:
            self.logger.error(
                f"Failed to generate chat completion: {e}", exc_info=True)
            raise

    async def generate_embedding(
        self, input_texts: List[str], embedding_model: Optional[str] = None
    ) -> List[List[float]]:
        """
        Generates embeddings for a list of input texts.

        Args:
            input_texts: A list of strings to embed.
            embedding_model: The specific model to use for embeddings (provider-dependent).

        Returns:
            A list of embeddings (each embedding is a list of floats).
        """
        if self.provider == "mock":
            self.logger.info(
                f"Mocking embeddings for texts: {input_texts[:2]}...")
            # Return fixed-size dummy embeddings
            return [
                [0.01 *
                    i for i in range(self.config.embedding_dimension_mock or 128)]
                for _ in input_texts
            ]

        model_to_use = embedding_model
        endpoint = ""
        payload: Dict[str, Any] = {}

        if self.provider == "openai":
            endpoint = "embeddings"
            model_to_use = model_to_use or self.config.openai_embedding_model
            if not model_to_use:
                raise LLMManagerError("OpenAI embedding model not configured.")
            payload = {"input": input_texts, "model": model_to_use}
        elif self.provider == "ollama":
            # Ollama's /api/embeddings endpoint
            endpoint = "embeddings"
            model_to_use = (
                model_to_use or self.config.ollama_embedding_model
            )  # Use a specific embedding model for Ollama
            if not model_to_use:
                raise LLMManagerError(
                    "Ollama embedding model not configured (e.g., nomic-embed-text, mxbai-embed-large)."
                )
            # Ollama /api/embeddings expects one prompt (text) at a time, or model and prompt. Iterate if multiple.
            # For simplicity, we'll make one call if input_texts has one item, else error or implement iteration.
            # Let's assume for now we'll call it per text if that's the API constraint.
            # Actually, the /api/embeddings endpoint for Ollama takes a single "prompt" string.
            # To handle multiple texts, we would need to call it multiple times or find a batch solution if available.
            # For now, let's raise an error if multiple texts are given for Ollama to simplify, or process one by one.

            # Simplified: Process one by one (can be inefficient)
            all_embeddings = []
            for text in input_texts:
                payload = {"model": model_to_use, "prompt": text}
                response_data = await self._make_request(endpoint, payload)
                if "embedding" not in response_data:
                    raise LLMManagerError(
                        f"Ollama embedding response missing 'embedding' key: {response_data}"
                    )
                all_embeddings.append(response_data["embedding"])
            return all_embeddings

        elif self.provider == "deepseek":
            # DeepSeek目前不提供专门的embedding API
            # 使用回退机制：如果配置了OpenAI API key，使用OpenAI的embedding
            # 否则建议使用本地embedding模型
            if self.config.openai_api_key:
                self.logger.warning(
                    "DeepSeek不支持embedding API，使用OpenAI embedding作为回退方案"
                )
                # 临时切换到OpenAI进行embedding
                temp_provider = self.provider
                temp_api_key = self.api_key
                temp_base_url = self.base_url

                self.provider = "openai"
                self.api_key = self.config.openai_api_key
                self.base_url = "https://api.openai.com/v1"

                try:
                    endpoint = "embeddings"
                    model_to_use = self.config.openai_embedding_model
                    payload = {"input": input_texts, "model": model_to_use}
                    response_data = await self._make_request(endpoint, payload)

                    # 恢复原设置
                    self.provider = temp_provider
                    self.api_key = temp_api_key
                    self.base_url = temp_base_url

                    if "data" in response_data and isinstance(
                        response_data["data"], list
                    ):
                        embeddings = [
                            item["embedding"] for item in response_data["data"]
                        ]
                        return embeddings
                    else:
                        raise LLMManagerError(
                            f"Unexpected embedding response format: {response_data}"
                        )
                except Exception as e:
                    # 恢复原设置
                    self.provider = temp_provider
                    self.api_key = temp_api_key
                    self.base_url = temp_base_url
                    raise LLMManagerError(
                        f"Failed to get embeddings using OpenAI fallback: {e}"
                    )
            else:
                raise LLMManagerError(
                    "DeepSeek不支持embedding API。请配置OPENAI_API_KEY作为embedding回退方案，"
                    "或使用sentence-transformers等本地embedding模型。"
                )
        else:
            raise LLMManagerError(
                f"Embedding generation not implemented for provider: {self.provider}"
            )

        try:
            response_data = await self._make_request(endpoint, payload)

            # Standardize response for OpenAI-like embedding APIs
            if "data" in response_data and isinstance(response_data["data"], list):
                embeddings = [item["embedding"]
                              for item in response_data["data"]]
                return embeddings
            else:
                raise LLMManagerError(
                    f"Unexpected embedding response format: {response_data}"
                )
        except LLMManagerError as e:
            self.logger.error(
                f"Failed to generate embeddings: {e}", exc_info=True)
            raise

    async def extract_core_research_params(
        self, query: str
    ) -> Dict[str, Optional[str]]:
        """
        Extract key research parameters from a natural language query.

        Args:
            query: The user's natural language research query

        Returns:
            Dictionary containing extracted parameters: topic, time_limit, focus
        """
        system_prompt = """Extract research parameters and translate Chinese to English. Return only JSON.

Parameters:
- topic: main subject (English)
- time_limit: time constraint (English)
- focus: specific aspects (English)

Examples:
"machine learning in healthcare 2020-2023" → {"topic": "machine learning in healthcare", "time_limit": "2020 to 2023", "focus": null}
"quantum computing cryptography since 2020" → {"topic": "quantum computing in cryptography", "time_limit": "since 2020", "focus": null}
"深度学习最新研究" → {"topic": "deep learning", "time_limit": "recent", "focus": null}
"量子计算在密码学中的应用" → {"topic": "quantum computing in cryptography", "time_limit": null, "focus": "applications"}"""

        user_prompt = f'"{query}" → '

        try:
            response_text = await self.generate_completion(
                prompt=user_prompt,
                system_prompt=system_prompt,
                max_tokens=500,
                temperature=0.1,
            )

            if not response_text:
                self.logger.error(
                    "No response from LLM for parameter extraction")
                # Use fallback translation
                return self._fallback_chinese_translation(query)

            # Try to parse JSON response
            import json
            import re

            try:
                # Clean the response to extract JSON
                response_text = response_text.strip()
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                response_text = response_text.strip()

                # Try to extract JSON from response using regex as backup
                json_match = re.search(r'\{[^{}]*\}', response_text)
                if json_match:
                    response_text = json_match.group()

                parsed_params = json.loads(response_text)

                # Validate required fields
                if not isinstance(parsed_params, dict):
                    raise ValueError("Response is not a dictionary")

                # Ensure we have the required keys with proper defaults
                result = {
                    "topic": parsed_params.get("topic") or query,
                    "time_limit": parsed_params.get("time_limit"),
                    "focus": parsed_params.get("focus"),
                }

                self.logger.info(
                    f"Successfully extracted parameters: {result}")
                return result

            except (json.JSONDecodeError, ValueError) as e:
                self.logger.warning(
                    f"Failed to parse JSON response: {e}. Response: {response_text}"
                )
                # Fallback: simple pattern matching for Chinese queries
                return self._fallback_chinese_translation(query)

        except Exception as e:
            self.logger.error(f"Error extracting research parameters: {e}")
            # Fallback: simple pattern matching for Chinese queries
            return self._fallback_chinese_translation(query)

    def _fallback_chinese_translation(self, query: str) -> Dict[str, Optional[str]]:
        """Simple pattern matching for common Chinese research queries."""
        import re
        query_lower = query.lower()
        
        # Time patterns
        time_limit = None
        if "2020" in query:
            if "以来" in query or "since" in query_lower:
                time_limit = "since 2020"
            elif "2021" in query or "2022" in query or "2023" in query or "2024" in query:
                # Extract year range if present
                years = re.findall(r'20\d{2}', query)
                if len(years) >= 2:
                    time_limit = f"{years[0]} to {years[-1]}"
                else:
                    time_limit = "since 2020"
        elif "最新" in query or "recent" in query_lower:
            time_limit = "recent"
        
        # Topic translation
        topic = query
        if "量子计算" in query and "密码" in query:
            topic = "quantum computing in cryptography"
        elif "深度学习" in query:
            topic = "deep learning"
        elif "机器学习" in query:
            topic = "machine learning"
        elif "人工智能" in query:
            topic = "artificial intelligence"
        elif "区块链" in query:
            topic = "blockchain"
        elif "神经网络" in query:
            topic = "neural networks"
        # Add the time constraint to topic if present
        if time_limit and time_limit not in topic:
            if "since" in time_limit:
                topic += f" {time_limit.replace('since', 'from')}"
        
        return {"topic": topic, "time_limit": time_limit, "focus": None}

    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> Optional[str]:
        """
        Generate a text completion using the configured LLM.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text completion or None if failed
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self.generate_chat_completion(
                messages=messages, max_tokens=max_tokens, temperature=temperature
            )

            if (
                response
                and response.get("choices")
                and response["choices"][0].get("message")
            ):
                message = response["choices"][0]["message"]
                content = message.get("content", "").strip()

                # For deepseek-reasoner, also log the reasoning process
                if self.model_name == "deepseek-reasoner" and message.get("reasoning_content"):
                    reasoning = message.get("reasoning_content", "").strip()
                    self.logger.debug(
                        f"DeepSeek Reasoning Process: {reasoning[:200]}...")
                    # Return the final answer, not the reasoning process

                return content
            else:
                self.logger.error(f"Invalid response format: {response}")
                return None

        except Exception as e:
            self.logger.error(f"Error generating completion: {e}")
            return None


if __name__ == "__main__":
    # Basic test for LLMManager
    import asyncio

    async def test_llm_manager():
        print("Testing LLMManager...")

        # Test with MOCK provider first (no API keys needed)
        print("\n--- Testing MOCK Provider ---")
        mock_config = Config(
            llm_provider="mock", openai_api_key=""
        )  # Ensure other keys aren't accidentally used
        mock_llm = LLMManager(config=mock_config)

        completion = await mock_llm.generate_chat_completion(
            messages=[{"role": "user", "content": "Hello Mock!"}]
        )
        print(
            f"Mock Completion: {completion['choices'][0]['message']['content']}")

        embeddings = await mock_llm.generate_embedding(
            input_texts=["Test text 1", "Test text 2"]
        )
        print(
            f"Mock Embeddings (first item, first 5 dims): {embeddings[0][:5]}...")
        print(f"Number of mock embeddings: {len(embeddings)}")

        # --- Test with OpenAI (requires OPENAI_API_KEY in .env or config) ---
        # Be cautious running this part if you don't want to use API credits.
        # It will only run if llm_provider is explicitly set to 'openai' in a Config object for testing.
        # And an API key is present.
        print(
            "\n--- Testing OpenAI Provider (SKIPPED if API key not found or provider not OpenAI) ---"
        )
        try:
            # Create a config that explicitly tries to use OpenAI for testing
            # It will read from .env or default values in Config
            openai_test_config = Config()  # This will load from .env
            if (
                openai_test_config.llm_provider == "openai"
                and openai_test_config.openai_api_key
            ):
                print(
                    f"OpenAI API Key found, proceeding with OpenAI test using model {openai_test_config.openai_model}..."
                )
                openai_llm = LLMManager(config=openai_test_config)

                # Test Chat Completion
                # print("Testing OpenAI Chat Completion...")
                # try:
                #     openai_completion = await openai_llm.generate_chat_completion(
                #         messages=[{"role": "user", "content": "What is the capital of France?"}],
                #         max_tokens=50
                #     )
                #     print(f"OpenAI Completion: {openai_completion['choices'][0]['message']['content']}")
                # except LLMManagerError as e:
                #     print(f"OpenAI Chat Completion failed: {e}")

                # Test Embedding
                print("Testing OpenAI Embedding...")
                try:
                    openai_embeddings = await openai_llm.generate_embedding(
                        input_texts=["Hello world", "Another test"]
                    )
                    print(
                        f"OpenAI Embeddings (first item, first 5 dims): {openai_embeddings[0][:5]}..."
                    )
                    print(
                        f"Number of OpenAI embeddings: {len(openai_embeddings)}")
                except LLMManagerError as e:
                    print(f"OpenAI Embedding failed: {e}")
            else:
                print(
                    "Skipping OpenAI tests: Provider is not 'openai' or API key not found in config."
                )
        except LLMManagerError as e:
            print(f"Could not initialize OpenAI LLMManager for test: {e}")
        except Exception as e:
            print(
                f"An unexpected error occurred during OpenAI test setup: {e}")

    asyncio.run(test_llm_manager())
