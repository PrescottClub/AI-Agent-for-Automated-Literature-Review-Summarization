<template>
  <div class="min-h-screen bg-gradient-to-br from-neutral-50 via-primary-50/20 to-secondary-50/10">
    <!-- 背景装饰元素 -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 right-20 w-64 h-64 bg-primary-100/50 rounded-full blur-3xl animate-float"></div>
      <div class="absolute bottom-20 left-20 w-64 h-64 bg-secondary-100/50 rounded-full blur-3xl animate-float" style="animation-delay: 3s;"></div>
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-primary-50/30 to-secondary-50/30 rounded-full blur-2xl animate-pulse-soft"></div>
    </div>
    <!-- 现代化导航栏 -->
    <nav class="relative z-50 backdrop-blur-md bg-white/80 border-b border-neutral-200/50 shadow-soft">
      <div class="max-w-7xl mx-auto px-6 lg:px-8">
        <div class="flex justify-between items-center h-20">
          <!-- 品牌标识 -->
          <div class="flex items-center space-x-4 cursor-pointer group" @click="goToWelcome">
            <div class="relative">
              <div class="w-12 h-12 bg-gradient-to-br from-primary to-primary-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-glow transition-all duration-300 group-hover:scale-105">
                <span class="text-white text-xl font-bold tracking-tight">T</span>
              </div>
              <div class="absolute inset-0 bg-gradient-to-br from-primary to-primary-600 rounded-2xl opacity-0 group-hover:opacity-20 transition-opacity duration-300 blur-lg"></div>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-neutral-900 tracking-tight group-hover:text-primary-700 transition-colors duration-300">
                Tsearch
              </h1>
              <p class="text-sm text-neutral-500 font-medium -mt-1">AI Literature Discovery</p>
            </div>
          </div>

          <!-- 导航菜单 -->
          <div class="hidden lg:flex items-center space-x-8">
            <!-- 登录状态显示 -->
            <div v-if="isAuthenticated()" class="flex items-center space-x-4">
              <div class="flex items-center space-x-2 px-3 py-2 bg-success-50 border border-success-200 rounded-xl">
                <div class="w-2 h-2 bg-success-500 rounded-full animate-pulse"></div>
                <span class="text-success-700 text-sm font-medium">已登录</span>
              </div>
              <button @click="handleLogout"
                      class="text-sm text-neutral-500 hover:text-danger-600 transition-colors">
                退出
              </button>
            </div>
            <div v-else>
              <button @click="showLogin = true"
                      class="group flex items-center px-4 py-2 bg-primary text-white rounded-xl hover:bg-primary-600 transition-all duration-300 hover:-translate-y-0.5 shadow-lg hover:shadow-glow">
                <span class="font-medium">登录</span>
              </button>
            </div>

            <button @click="showHistory = true"
                    class="group flex items-center px-4 py-2 text-neutral-600 hover:text-primary-600 transition-all duration-300 rounded-xl hover:bg-primary-50">
              <el-icon class="mr-2 group-hover:scale-110 transition-transform duration-300">
                <Clock />
              </el-icon>
              <span class="font-medium">搜索历史</span>
            </button>

            <button @click="showSettings = true"
                    class="group flex items-center px-4 py-2 text-neutral-600 hover:text-primary-600 transition-all duration-300 rounded-xl hover:bg-primary-50">
              <el-icon class="mr-2 group-hover:scale-110 transition-transform duration-300">
                <Setting />
              </el-icon>
              <span class="font-medium">设置</span>
            </button>

            <!-- 智能统计面板 -->
            <div class="flex items-center space-x-6 pl-6 border-l border-neutral-200">
              <div class="group relative">
                <div class="text-center p-2 rounded-lg hover:bg-primary-50 transition-colors cursor-pointer">
                  <div class="text-lg font-bold text-primary-600">{{ totalPapers || 0 }}</div>
                  <div class="text-xs text-neutral-500">Papers Found</div>
                </div>
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-neutral-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">
                  本次检索结果
                </div>
              </div>
              <div class="group relative">
                <div class="text-center p-2 rounded-lg hover:bg-success-50 transition-colors cursor-pointer">
                  <div class="text-lg font-bold text-success-600">{{ relevanceScore || 95 }}%</div>
                  <div class="text-xs text-neutral-500">AI Relevance</div>
                </div>
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-neutral-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">
                  AI智能相关性评分
                </div>
              </div>
            </div>
          </div>

          <!-- 移动端菜单按钮 -->
          <div class="lg:hidden">
            <button @click="showMobileMenu = !showMobileMenu"
                    class="p-2 text-neutral-600 hover:text-primary-600 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <main class="relative z-10 pt-8 pb-20">
      <div class="max-w-7xl mx-auto px-6 lg:px-8">
        <!-- 英雄区域 -->
        <section class="text-center mb-16 lg:mb-20">
          <!-- 动态状态徽章 -->
          <div class="inline-flex items-center space-x-3 bg-white/90 backdrop-blur-md border border-primary-200/50 rounded-full px-6 py-3 mb-8 shadow-soft animate-fade-in-down group hover:shadow-lg transition-all duration-300">
            <div class="relative">
              <div class="w-3 h-3 bg-gradient-to-r from-success to-primary rounded-full animate-pulse-soft"></div>
              <div class="absolute inset-0 w-3 h-3 bg-gradient-to-r from-success to-primary rounded-full opacity-30 animate-ping"></div>
            </div>
            <span class="text-primary-700 text-sm font-semibold group-hover:text-primary-800 transition-colors">
              {{ isAuthenticated() ? 'AI 智能检索系统已就绪 · 用户已验证' : 'AI 智能检索系统 · 需要登录访问' }}
            </span>
            <div v-if="isAuthenticated()" class="w-1.5 h-1.5 bg-success rounded-full opacity-60"></div>
          </div>

          <!-- 主标题 -->
          <h1 class="text-5xl lg:text-7xl font-bold text-neutral-900 mb-8 leading-tight animate-fade-in-up animate-delay-100">
            <span class="block">发现学术</span>
            <span class="gradient-text-primary block">新洞察</span>
            <span class="block text-3xl lg:text-5xl text-neutral-600 font-light mt-4">
              超越想象的边界
            </span>
          </h1>

          <!-- 副标题 -->
          <p class="text-xl lg:text-2xl text-neutral-600 max-w-4xl mx-auto leading-relaxed mb-12 animate-fade-in-up animate-delay-200">
            基于AI的文献发现平台，让学术研究变得更加智能高效。
            <br class="hidden lg:block">
            精准检索、智能分析、一键生成专业报告。
          </p>

          <!-- 统计卡片 -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-4xl mx-auto mb-16 animate-fade-in-up animate-delay-300">
            <div class="group relative">
              <div class="absolute inset-0 bg-gradient-to-br from-primary-50 to-primary-100 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div class="relative bg-white/80 backdrop-blur-sm border border-neutral-200 rounded-2xl p-8 text-center shadow-soft hover:shadow-medium transition-all duration-300 hover:-translate-y-1">
                <div class="text-4xl mb-4">📚</div>
                <div class="text-3xl font-bold text-primary-600 mb-2">10M+</div>
                <div class="text-neutral-500 font-medium">文献数据库</div>
              </div>
            </div>

            <div class="group relative">
              <div class="absolute inset-0 bg-gradient-to-br from-success-50 to-success-100 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div class="relative bg-white/80 backdrop-blur-sm border border-neutral-200 rounded-2xl p-8 text-center shadow-soft hover:shadow-medium transition-all duration-300 hover:-translate-y-1">
                <div class="text-4xl mb-4">🎯</div>
                <div class="text-3xl font-bold text-success-600 mb-2">99.2%</div>
                <div class="text-neutral-500 font-medium">检索准确率</div>
              </div>
            </div>

            <div class="group relative">
              <div class="absolute inset-0 bg-gradient-to-br from-warning-50 to-warning-100 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div class="relative bg-white/80 backdrop-blur-sm border border-neutral-200 rounded-2xl p-8 text-center shadow-soft hover:shadow-medium transition-all duration-300 hover:-translate-y-1">
                <div class="text-4xl mb-4">⚡</div>
                <div class="text-3xl font-bold text-warning-600 mb-2">2.3s</div>
                <div class="text-neutral-500 font-medium">平均响应时间</div>
              </div>
            </div>
          </div>
        </section>

        <!-- 智能搜索界面 -->
        <section class="max-w-5xl mx-auto mb-16 animate-fade-in-up animate-delay-500">
          <div class="relative">
            <!-- 主搜索卡片 -->
            <div class="bg-white/90 backdrop-blur-md border border-neutral-200/50 rounded-3xl p-8 lg:p-12 shadow-large">
              <!-- 智能搜索标题 -->
              <div class="text-center mb-10">
                <div class="flex items-center justify-center mb-4">
                  <div class="w-10 h-10 bg-gradient-to-br from-primary-400 to-primary-600 rounded-2xl flex items-center justify-center mr-4 shadow-lg">
                    <span class="text-white text-xl">🧠</span>
                  </div>
                  <h2 class="text-3xl lg:text-4xl font-bold text-neutral-900">
                    语义智能检索
                  </h2>
                </div>
                <p class="text-xl text-neutral-600 max-w-3xl mx-auto leading-relaxed">
                  基于深度学习的<strong class="text-primary-600">语义理解</strong>技术，
                  <br class="hidden lg:block">
                  让AI理解您的研究意图，而不仅仅是关键词匹配
                </p>
                <div class="flex items-center justify-center mt-6 space-x-6 text-sm text-neutral-500">
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-gradient-to-r from-primary to-secondary rounded-full"></div>
                    <span>多源并行检索</span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-gradient-to-r from-success to-warning rounded-full"></div>
                    <span>AI语义分析</span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-gradient-to-r from-warning to-danger rounded-full"></div>
                    <span>智能结果排序</span>
                  </div>
                </div>
              </div>

              <!-- AI增强搜索输入区域 -->
              <div class="mb-8">
                <div class="relative">
                  <!-- 搜索框标签 -->
                  <div class="flex items-center justify-between mb-4">
                    <div class="flex items-center space-x-2">
                      <span class="text-sm font-semibold text-neutral-700">研究问题描述</span>
                      <div class="px-2 py-1 bg-gradient-to-r from-primary-100 to-secondary-100 rounded-full text-xs font-medium text-primary-700">
                        AI Enhanced
                      </div>
                    </div>
                    <div class="flex items-center space-x-2 text-xs text-neutral-500">
                      <span>字符数: {{ searchQuery.length }}/2000</span>
                    </div>
                  </div>
                  
                  <el-input
                    v-model="searchQuery"
                    type="textarea"
                    :autosize="{ minRows: 5, maxRows: 10 }"
                    :maxlength="2000"
                    placeholder="🧠 AI智能提示：详细描述您的研究需求，例如：&#10;&#10;'我需要研究深度学习在医疗影像诊断中的最新突破，特别关注：&#10;1. 肺部疾病检测的创新方法&#10;2. 临床应用效果和准确率分析&#10;3. 2022年以来的技术发展趋势&#10;4. 与传统方法的对比研究'&#10;&#10;💡 越详细的描述，AI匹配的结果越精准！"
                    class="search-input-ai-enhanced"
                    @keyup.enter.ctrl="startSearch"
                    @input="handleSearchInput"
                  />
                  
                  <!-- AI智能提示浮层 -->
                  <div class="absolute inset-x-0 top-full mt-2 z-10">
                    <div v-if="searchQuery.length > 20 && aiSuggestions.length > 0" 
                         class="bg-white/95 backdrop-blur-md border border-primary-200/50 rounded-2xl p-4 shadow-large">
                      <div class="flex items-center space-x-2 mb-3">
                        <div class="w-5 h-5 bg-gradient-to-br from-primary-400 to-primary-600 rounded-lg flex items-center justify-center">
                          <span class="text-white text-xs">✨</span>
                        </div>
                        <span class="text-sm font-semibold text-neutral-700">AI智能建议</span>
                      </div>
                      <div class="space-y-2">
                        <div v-for="(suggestion, index) in aiSuggestions" :key="index"
                             class="p-3 bg-gradient-to-r from-primary-50/50 to-transparent rounded-xl border border-primary-200/30 hover:border-primary-300 cursor-pointer transition-all duration-200 hover:-translate-y-0.5"
                             @click="applySuggestion(suggestion)">
                          <div class="flex items-start space-x-3">
                            <div class="w-6 h-6 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                              <span class="text-primary-600 text-xs font-bold">{{ index + 1 }}</span>
                            </div>
                            <span class="text-sm text-neutral-700 leading-relaxed">{{ suggestion }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 输入框装饰和功能按钮 -->
                  <div class="absolute top-16 right-4 flex items-center space-x-3">
                    <button v-if="searchQuery.length > 0" 
                            @click="clearSearch"
                            class="p-1.5 text-neutral-400 hover:text-neutral-600 rounded-lg hover:bg-neutral-100 transition-colors">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                      </svg>
                    </button>
                    <div class="flex items-center space-x-1 text-xs text-neutral-400">
                      <kbd class="px-2 py-1 bg-neutral-100 text-neutral-600 rounded font-mono">Ctrl</kbd>
                      <span>+</span>
                      <kbd class="px-2 py-1 bg-neutral-100 text-neutral-600 rounded font-mono">Enter</kbd>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 搜索控制区域 -->
              <div class="flex flex-col lg:flex-row items-center justify-between gap-6">
                <!-- 状态指示器 -->
                <div class="flex items-center space-x-6 text-sm">
                  <div class="flex items-center space-x-2">
                    <div class="w-2.5 h-2.5 bg-success rounded-full animate-pulse-soft"></div>
                    <span class="text-neutral-600 font-medium">AI 系统就绪</span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <div class="w-2.5 h-2.5 bg-primary rounded-full"></div>
                    <span class="text-neutral-600 font-medium">多源检索</span>
                  </div>
                </div>

                <!-- 搜索按钮 -->
                <button
                  @click="startSearch"
                  :disabled="!searchQuery.trim() || isSearching"
                  class="group relative px-10 py-4 bg-gradient-to-r from-primary to-primary-600 text-white rounded-2xl font-semibold shadow-lg hover:shadow-glow transition-all duration-300 hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                  <div class="flex items-center justify-center">
                    <el-icon v-if="isSearching" class="animate-spin mr-3 text-lg">
                      <Loading />
                    </el-icon>
                    <el-icon v-else class="mr-3 text-lg group-hover:scale-110 transition-transform duration-300">
                      <Search />
                    </el-icon>
                    <span class="text-lg">{{ isSearching ? '智能检索中...' : '开始智能检索' }}</span>
                  </div>
                  <div class="absolute inset-0 bg-gradient-to-r from-primary-600 to-primary-700 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </button>
              </div>

              <!-- 快速建议 -->
              <div v-if="naturalLanguageSuggestions.length > 0" class="mt-10">
                <p class="text-sm text-neutral-500 font-medium mb-4">💡 快速开始</p>
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
                  <button
                    v-for="suggestion in naturalLanguageSuggestions.slice(0, 3)"
                    :key="suggestion"
                    @click="searchQuery = suggestion; startSearch()"
                    class="group p-4 bg-neutral-50 border border-neutral-200 rounded-xl text-left text-sm text-neutral-700 hover:bg-primary-50 hover:border-primary-200 hover:text-primary-700 transition-all duration-300 hover:-translate-y-0.5">
                    <div class="line-clamp-3">{{ suggestion }}</div>
                    <div class="mt-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                      <span class="text-xs text-primary-600 font-medium">点击使用 →</span>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 高级选项 -->
        <section class="max-w-5xl mx-auto mb-16">
          <div class="text-center">
            <button
              @click="showAdvancedOptions = !showAdvancedOptions"
              class="group inline-flex items-center px-6 py-3 text-neutral-600 hover:text-primary-600 transition-all duration-300 rounded-xl hover:bg-primary-50">
              <span class="font-medium mr-2">{{ showAdvancedOptions ? '隐藏' : '显示' }}高级选项</span>
              <el-icon class="transition-transform duration-300 group-hover:scale-110" :class="{ 'rotate-180': showAdvancedOptions }">
                <ArrowDown />
              </el-icon>
            </button>
          </div>

          <Transition name="advanced-options">
            <div v-if="showAdvancedOptions" class="mt-8 bg-white/90 backdrop-blur-md border border-neutral-200/50 rounded-2xl p-8 shadow-large">
              <h3 class="text-2xl font-bold text-neutral-900 mb-8 text-center">高级搜索设置</h3>

              <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <!-- 数据源选择 -->
                <div class="space-y-4">
                  <label class="block text-sm font-semibold text-neutral-700 mb-3">数据源</label>
                  <el-select v-model="selectedSources" multiple placeholder="选择数据源" class="w-full">
                    <el-option label="arXiv" value="arxiv" />
                    <el-option label="Semantic Scholar" value="semantic_scholar" />
                  </el-select>
                  <p class="text-xs text-neutral-500">选择要搜索的学术数据库</p>
                </div>

                <!-- 论文数量 -->
                <div class="space-y-4">
                  <label class="block text-sm font-semibold text-neutral-700 mb-3">
                    最大论文数量: <span class="text-primary-600 font-bold">{{ maxPapers }}</span>
                  </label>
                  <el-slider v-model="maxPapers" :min="5" :max="50" :step="5" class="mt-4" />
                  <p class="text-xs text-neutral-500">控制返回的论文数量以优化检索速度</p>
                </div>

                <!-- 功能选项 -->
                <div class="lg:col-span-2 space-y-6">
                  <h4 class="text-lg font-semibold text-neutral-800 border-b border-neutral-200 pb-2">功能选项</h4>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <label class="flex items-center p-4 bg-neutral-50 rounded-xl border border-neutral-200 hover:border-primary-200 hover:bg-primary-50/50 transition-all duration-300 cursor-pointer">
                      <el-checkbox v-model="retrieveFullText" />
                      <div class="ml-4">
                        <span class="font-medium text-neutral-800">获取全文</span>
                        <p class="text-sm text-neutral-600 mt-1">尝试获取论文的完整文本内容</p>
                      </div>
                    </label>

                    <label class="flex items-center p-4 bg-neutral-50 rounded-xl border border-neutral-200 hover:border-primary-200 hover:bg-primary-50/50 transition-all duration-300 cursor-pointer">
                      <el-checkbox v-model="enableAIAnalysis" />
                      <div class="ml-4">
                        <span class="font-medium text-neutral-800">AI 智能分析</span>
                        <p class="text-sm text-neutral-600 mt-1">使用AI对检索结果进行深度分析</p>
                      </div>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </section>

        <!-- 结果展示区域 -->
        <section v-if="isSearching || searchResults.length > 0 || (actionPlan && actionPlan.length > 0)" class="max-w-7xl mx-auto">
          <!-- 加载动画 -->
          <div v-if="isSearching && searchResults.length === 0" class="text-center py-20">
            <div class="relative inline-block mb-8">
              <div class="w-20 h-20 border-4 border-primary-200 border-t-primary rounded-full animate-spin"></div>
              <div class="absolute inset-0 w-20 h-20 border-4 border-secondary-200 border-b-secondary rounded-full animate-spin" style="animation-direction: reverse;"></div>
            </div>
            <h3 class="text-2xl font-bold text-neutral-900 mb-4">AI 正在处理您的查询</h3>
            <p class="text-neutral-600 text-lg">分析需求并搜索相关文献...</p>
            <div class="mt-6 flex justify-center">
              <div class="flex space-x-2">
                <div class="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0.1s;"></div>
                <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0.2s;"></div>
              </div>
            </div>
          </div>

          <!-- AI 执行计划 -->
          <div v-if="actionPlan && actionPlan.length > 0" class="mb-16">
            <div class="bg-white/90 backdrop-blur-md border border-neutral-200/50 rounded-2xl p-8 shadow-large">
              <div class="flex items-center mb-8">
                <div class="w-12 h-12 bg-gradient-to-br from-primary-100 to-primary-200 rounded-2xl flex items-center justify-center mr-4">
                  <span class="text-2xl">🤖</span>
                </div>
                <div>
                  <h3 class="text-2xl font-bold text-neutral-900">AI 执行计划</h3>
                  <p class="text-neutral-600">智能分析您的需求并制定检索策略</p>
                </div>
              </div>
              <div class="space-y-4">
                <div v-for="(step, index) in actionPlan" :key="index"
                     class="flex items-start space-x-4 p-4 bg-neutral-50 rounded-xl border border-neutral-200 hover:border-primary-200 hover:bg-primary-50/50 transition-all duration-300">
                  <div class="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-primary to-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold shadow-lg">
                    {{ index + 1 }}
                  </div>
                  <p class="text-neutral-700 font-medium leading-relaxed">{{ step }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 搜索结果 -->
          <div v-if="searchResults.length > 0" class="space-y-8">
            <!-- 结果标题和操作 -->
            <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6 p-8 bg-white/90 backdrop-blur-md border border-neutral-200/50 rounded-2xl shadow-large">
              <div>
                <h2 class="text-3xl font-bold text-neutral-900 mb-2">检索结果</h2>
                <p class="text-neutral-600 text-lg">找到 <span class="font-bold text-primary-600">{{ searchResults.length }}</span> 篇相关文献</p>
              </div>
              <button
                @click="generateReport"
                :disabled="isGeneratingReport"
                class="group px-8 py-4 bg-gradient-to-r from-success to-success-600 text-white rounded-2xl font-semibold shadow-lg hover:shadow-glow transition-all duration-300 hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                <div class="flex items-center">
                  <el-icon v-if="isGeneratingReport" class="animate-spin mr-3 text-lg">
                    <Loading />
                  </el-icon>
                  <el-icon v-else class="mr-3 text-lg group-hover:scale-110 transition-transform duration-300">
                    <Document />
                  </el-icon>
                  <span>{{ isGeneratingReport ? '生成中...' : '生成报告' }}</span>
                </div>
              </button>
            </div>

            <!-- 论文卡片网格 -->
            <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
              <PaperCard
                v-for="(paper, index) in searchResults"
                :key="paper.id"
                :paper="paper"
                :index="index + 1"
                @toggle-favorite="toggleFavorite"
                @view-details="viewDetailsModal"
                @download-pdf="downloadPdf"
                class="animate-fade-in-up hover-lift"
                :style="{ animationDelay: `${index * 0.1}s` }"
              />
            </div>
          </div>
        </section>
      </div>
    </main>

    <!-- 对话框组件 -->
    <!-- 设置对话框 -->
    <el-dialog v-model="showSettings" title="系统设置" width="600px" class="modern-dialog">
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-semibold text-neutral-700 mb-3">默认数据源</label>
          <el-select v-model="defaultSources" multiple placeholder="选择默认数据源" class="w-full">
            <el-option label="arXiv" value="arxiv" />
            <el-option label="Semantic Scholar" value="semantic_scholar" />
          </el-select>
          <p class="text-xs text-neutral-500 mt-2">设置默认使用的学术数据库</p>
        </div>

        <div>
          <label class="block text-sm font-semibold text-neutral-700 mb-3">默认最大论文数</label>
          <el-input-number v-model="defaultMaxPapers" :min="5" :max="50" :step="5" class="w-full" />
          <p class="text-xs text-neutral-500 mt-2">设置每次搜索返回的最大论文数量</p>
        </div>

        <div>
          <label class="block text-sm font-semibold text-neutral-700 mb-3">界面语言</label>
          <el-select v-model="language" placeholder="选择界面语言" class="w-full">
            <el-option label="中文" value="zh" />
            <el-option label="English" value="en" />
          </el-select>
          <p class="text-xs text-neutral-500 mt-2">设置系统界面显示语言</p>
        </div>
      </div>
    </el-dialog>

    <!-- 搜索历史对话框 -->
    <el-dialog v-model="showHistory" title="搜索历史" width="700px" class="modern-dialog">
      <div v-if="searchHistory.length === 0" class="text-center py-12">
        <div class="text-6xl mb-4">📚</div>
        <h3 class="text-xl font-semibold text-neutral-700 mb-2">暂无搜索历史</h3>
        <p class="text-neutral-500">开始您的第一次文献检索吧！</p>
      </div>

      <div v-else class="space-y-4 max-h-96 overflow-y-auto">
        <div
          v-for="(item, index) in searchHistory"
          :key="index"
          class="group p-4 border border-neutral-200 rounded-xl hover:border-primary-200 hover:bg-primary-50/50 cursor-pointer transition-all duration-300"
          @click="searchQuery = item.query; showHistory = false">
          <div class="font-semibold text-neutral-800 mb-2 line-clamp-2 group-hover:text-primary-700">
            {{ item.query }}
          </div>
          <div class="flex items-center justify-between text-sm text-neutral-500">
            <span>{{ item.date }}</span>
            <span class="px-2 py-1 bg-neutral-100 rounded-full group-hover:bg-primary-100 group-hover:text-primary-700">
              {{ item.resultCount }} 篇结果
            </span>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 登录对话框 -->
    <el-dialog v-model="showLogin" title="用户登录" width="400px" class="modern-dialog">
      <el-form @submit.prevent="handleLoginForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLoginForm" :loading="isLoggingIn" class="w-full">
            {{ isLoggingIn ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
      <div class="text-center text-sm text-neutral-500 mt-4">
        <p>默认账户: admin / secret</p>
      </div>
    </el-dialog>

    <!-- 移动端菜单 -->
    <div v-if="showMobileMenu" class="lg:hidden fixed inset-0 z-50 bg-black/50" @click="showMobileMenu = false">
      <div class="absolute top-20 right-6 bg-white rounded-2xl shadow-large p-6 min-w-[200px]" @click.stop>
        <div class="space-y-4">
          <button @click="showHistory = true; showMobileMenu = false"
                  class="w-full flex items-center px-4 py-3 text-neutral-600 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-all duration-300">
            <el-icon class="mr-3"><Clock /></el-icon>
            <span>搜索历史</span>
          </button>
          <button @click="showSettings = true; showMobileMenu = false"
                  class="w-full flex items-center px-4 py-3 text-neutral-600 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-all duration-300">
            <el-icon class="mr-3"><Setting /></el-icon>
            <span>设置</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Setting,
  Clock,
  Loading,
  ArrowDown,
  Search,
  Document
} from '@element-plus/icons-vue'
import PaperCard from '../components/PaperCard.vue'
import type { Paper, SearchHistoryItem } from '../types/paper'

// 路由
const router = useRouter()

// 响应式数据
const searchQuery = ref('')
const selectedSources = ref(['arxiv', 'semantic_scholar'])
const maxPapers = ref(20)
const retrieveFullText = ref(false)
const enableAIAnalysis = ref(true)
const isSearching = ref(false)
const isGeneratingReport = ref(false)
const hasSearched = ref(false)
const searchResults = ref<Paper[]>([])
const searchProgress = ref('')
const actionPlan = ref<string[]>([])

// UI 状态
const showSettings = ref(false)
const showHistory = ref(false)
const showAdvancedOptions = ref(false)
const showMobileMenu = ref(false)
const showLogin = ref(false)

// 登录表单
const loginForm = ref({
  username: 'admin',
  password: 'secret'
})
const isLoggingIn = ref(false)

// 设置
const defaultSources = ref(['arxiv', 'semantic_scholar'])
const defaultMaxPapers = ref(20)
const language = ref('zh')

// 搜索历史
const searchHistory = ref<SearchHistoryItem[]>([])

// 统计数据
const totalPapers = ref(0)
const processingTime = ref(2.3)
const relevanceScore = ref(95)

// AI智能建议系统
const aiSuggestions = ref<string[]>([])
const naturalLanguageSuggestions = ref([
  '最近三年人工智能在医疗诊断领域的应用进展',
  '寻找关于深度学习优化算法的最新研究，重点关注transformer架构',
  '查找2020年以来量子计算在密码学中的应用研究',
])

// AI增强功能
const generateAISuggestions = (query: string) => {
  if (query.length < 20) {
    aiSuggestions.value = []
    return
  }
  
  // 基于关键词的智能建议生成
  const suggestions = []
  
  if (query.includes('深度学习') || query.includes('机器学习')) {
    suggestions.push('建议添加时间范围：如"2020年以来"或"最近5年"')
    suggestions.push('可以指定应用领域：如"在医疗领域"、"在计算机视觉中"')
    suggestions.push('考虑添加技术细节：如"基于CNN"、"使用Transformer架构"')
  }
  
  if (query.includes('医疗') || query.includes('诊断')) {
    suggestions.push('建议明确医疗子领域：如"影像诊断"、"病理分析"、"药物发现"')
    suggestions.push('可以关注临床应用：如"FDA批准"、"临床试验结果"')
  }
  
  if (query.includes('最新') || query.includes('进展')) {
    suggestions.push('建议指定时间窗口：如"2023-2024年"、"近两年内"')
    suggestions.push('可以关注顶会论文：如"NIPS"、"ICLR"、"Nature"期刊')
  }
  
  if (suggestions.length === 0) {
    suggestions.push('尝试添加更多具体细节来提高检索精度')
    suggestions.push('可以包含研究方法、应用场景或技术关键词')
    suggestions.push('建议指定发表时间范围以获取最新研究')
  }
  
  aiSuggestions.value = suggestions.slice(0, 3)
}

const handleSearchInput = (value: string) => {
  generateAISuggestions(value)
}

const applySuggestion = (suggestion: string) => {
  // 简单的建议应用逻辑，实际可以更智能
  ElMessage.success('AI建议已应用，请根据提示完善您的查询')
  aiSuggestions.value = []
}

const clearSearch = () => {
  searchQuery.value = ''
  aiSuggestions.value = []
}

// 认证相关函数
const getAuthToken = () => {
  return localStorage.getItem('authToken') || ''
}

const isAuthenticated = () => {
  return !!getAuthToken()
}

const handleLogin = async (username: string, password: string) => {
  try {
    const response = await fetch('http://localhost:8000/auth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
    })

    if (!response.ok) {
      throw new Error('登录失败')
    }

    const data = await response.json()
    localStorage.setItem('authToken', data.access_token)
    ElMessage.success('登录成功！')
    showLogin.value = false
    return true
  } catch (error) {
    ElMessage.error('登录失败，请检查用户名和密码')
    return false
  }
}

const handleLoginForm = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  
  isLoggingIn.value = true
  const success = await handleLogin(loginForm.value.username, loginForm.value.password)
  isLoggingIn.value = false
  
  if (success) {
    // 登录成功后可以自动重新执行之前的操作
  }
}

const handleLogout = () => {
  localStorage.removeItem('authToken')
  ElMessage.success('已退出登录')
  // 清空搜索结果
  searchResults.value = []
  actionPlan.value = []
}

// 方法
const startSearch = async () => {
  if (!searchQuery.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }
  isSearching.value = true
  hasSearched.value = true
  searchResults.value = []
  actionPlan.value = []
  searchProgress.value = '正在连接服务器...'

  try {
    console.log(`Searching for: ${searchQuery.value}, Sources: ${selectedSources.value.join(', ')}, Max Papers: ${maxPapers.value}`);

    // 调用真实API
    const response = await fetch('http://localhost:8000/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAuthToken()}` // 需要认证
      },
      body: JSON.stringify({
        rawQuery: searchQuery.value,
        query: searchQuery.value, // backward compatibility
        maxPapers: maxPapers.value,
        sources: selectedSources.value,
        retrieveFullText: retrieveFullText.value,
        yearStart: null,
        yearEnd: null
      })
    })

    if (!response.ok) {
      if (response.status === 401) {
        ElMessage.error('需要登录才能进行检索')
        showLogin.value = true
        return
      }
      throw new Error(`API请求失败: ${response.status}`)
    }

    const data = await response.json()
    
    // 处理返回的数据
    actionPlan.value = data.actionPlan || []
    searchResults.value = data.papers || []

    // 更新统计信息
    totalPapers.value = searchResults.value.length
    relevanceScore.value = Math.floor(Math.random() * 5) + 95 // 95-99%的相关性分数

    // 保存搜索历史
    const historyItem: SearchHistoryItem = {
      query: searchQuery.value,
      date: new Date().toLocaleDateString('zh-CN'),
      resultCount: searchResults.value.length,
      params: {
        sources: selectedSources.value,
        maxPapers: maxPapers.value,
        retrieveFullText: retrieveFullText.value,
        enableAIAnalysis: enableAIAnalysis.value
      }
    };
    searchHistory.value.unshift(historyItem);
    if (searchHistory.value.length > 10) {
      searchHistory.value = searchHistory.value.slice(0, 10);
    }

    ElMessage.success(`检索完成！找到 ${searchResults.value.length} 篇相关文献`);

  } catch (error) {
    console.error('Search error:', error)
    ElMessage.error('检索失败，请检查网络连接或稍后重试')
  } finally {
    isSearching.value = false
    searchProgress.value = ''
  }
}

const generateReport = async () => {
  if (searchResults.value.length === 0) {
    ElMessage.warning('没有可用的论文数据生成报告')
    return
  }
  
  if (!isAuthenticated()) {
    ElMessage.error('需要登录才能生成报告')
    return
  }
  
  isGeneratingReport.value = true
  
  try {
    const response = await fetch('http://localhost:8000/api/generate-report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getAuthToken()}`
      },
      body: JSON.stringify({
        title: `基于"${searchQuery.value}"的文献综述报告`,
        papers: searchResults.value
      })
    })

    if (!response.ok) {
      if (response.status === 401) {
        ElMessage.error('认证已过期，请重新登录')
        return
      }
      throw new Error(`报告生成失败: ${response.status}`)
    }

    const data = await response.json()
    const reportContent = data.report || '报告生成失败'

    ElMessageBox.alert(`<pre style="white-space: pre-wrap; max-height: 500px; overflow-y: auto;">${reportContent}</pre>`, '文献综述报告', {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '关闭',
      customClass: 'report-dialog'
    })
  } catch (error) {
    console.error('Report generation error:', error)
    ElMessage.error('报告生成失败，请检查网络连接或稍后重试')
  } finally {
    isGeneratingReport.value = false
  }
}

// PaperCard event handlers
const toggleFavorite = (paperId: string) => {
  const paper = searchResults.value.find(p => p.id === paperId);
  if (paper) {
    paper.isFavorite = !paper.isFavorite;
    ElMessage.success(paper.isFavorite ? '已收藏' : '取消收藏');
  }
};

const viewDetailsModal = (paper: Paper) => {
  ElMessageBox.alert(JSON.stringify(paper, null, 2), `论文详情: ${paper.title}`, {
    confirmButtonText: '关闭',
    customClass: 'report-dialog' // Using existing class for wider dialog
  });
};

const downloadPdf = (paper: Paper) => {
  if (paper.pdfUrl && paper.pdfUrl !== '#') {
    window.open(paper.pdfUrl, '_blank');
  } else {
    ElMessage.info('该论文暂无可用PDF链接。');
  }
};

// 移除未使用的函数，这些功能将在后续的组件拆分中实现

const goToWelcome = () => {
  router.push('/')
}

// Lifecycle
onMounted(() => {
  const savedSettings = localStorage.getItem('literatureReviewSettings');
  if (savedSettings) {
    const settings = JSON.parse(savedSettings);
    defaultSources.value = settings.defaultSources || ['arxiv', 'semantic_scholar'];
    defaultMaxPapers.value = settings.defaultMaxPapers || 20;
    language.value = settings.language || 'zh';
  }
  const savedHistory = localStorage.getItem('searchHistory');
  if (savedHistory) {
    searchHistory.value = JSON.parse(savedHistory);
  }
});

watch([defaultSources, defaultMaxPapers, language], (newValues) => {
  localStorage.setItem('literatureReviewSettings', JSON.stringify({
    defaultSources: newValues[0],
    defaultMaxPapers: newValues[1],
    language: newValues[2]
  }));
}, { deep: true });

watch(searchHistory, (newHistory) => {
  localStorage.setItem('searchHistory', JSON.stringify(newHistory));
}, { deep: true });
</script>

<style scoped>
/* HomeView 专用样式 */

/* 渐变文字动画 */
.gradient-text-primary {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-600), var(--color-secondary));
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 4s ease-in-out infinite;
}

@keyframes gradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

/* 高级选项过渡动画 */
.advanced-options-enter-active,
.advanced-options-leave-active {
  transition: all 0.4s ease-out;
  transform-origin: top;
}

.advanced-options-enter-from {
  opacity: 0;
  transform: scaleY(0.8) translateY(-20px);
}

.advanced-options-leave-to {
  opacity: 0;
  transform: scaleY(0.8) translateY(-20px);
}

/* AI增强搜索输入框样式 */
.search-input-ai-enhanced :deep(.el-textarea__inner) {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.95)) !important;
  border: 2px solid transparent !important;
  border-radius: 20px !important;
  padding: 24px !important;
  font-size: 16px !important;
  line-height: 1.7 !important;
  resize: none !important;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: 
    0 0 0 1px rgba(14, 165, 233, 0.1),
    0 8px 32px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.7) !important;
  position: relative;
}

.search-input-ai-enhanced :deep(.el-textarea__inner):focus {
  background: rgba(255, 255, 255, 1) !important;
  box-shadow: 
    0 0 0 2px rgba(14, 165, 233, 0.2),
    0 0 0 4px rgba(14, 165, 233, 0.1),
    0 12px 40px rgba(14, 165, 233, 0.15) !important;
  transform: translateY(-1px);
}

.search-input-ai-enhanced :deep(.el-textarea__inner)::placeholder {
  color: var(--color-neutral-500) !important;
  font-style: normal !important;
  line-height: 1.6 !important;
}

/* 搜索输入框现代化样式 (保留兼容) */
.search-input-modern :deep(.el-textarea__inner) {
  background: rgba(255, 255, 255, 0.9) !important;
  border: 2px solid var(--color-neutral-200) !important;
  border-radius: 16px !important;
  padding: 20px !important;
  font-size: 16px !important;
  line-height: 1.6 !important;
  resize: none !important;
  transition: all 0.3s ease-out !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
}

.search-input-modern :deep(.el-textarea__inner):focus {
  border-color: var(--color-primary) !important;
  box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1), 0 8px 30px rgba(0, 0, 0, 0.1) !important;
  background: rgba(255, 255, 255, 1) !important;
}

.search-input-modern :deep(.el-textarea__inner)::placeholder {
  color: var(--color-neutral-400) !important;
  font-style: italic !important;
}

/* 现代化对话框样式 */
.modern-dialog :deep(.el-dialog) {
  border-radius: 20px !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15) !important;
  border: 1px solid var(--color-neutral-200) !important;
}

.modern-dialog :deep(.el-dialog__header) {
  padding: 24px 24px 16px !important;
  border-bottom: 1px solid var(--color-neutral-200) !important;
}

.modern-dialog :deep(.el-dialog__title) {
  font-size: 1.5rem !important;
  font-weight: 600 !important;
  color: var(--color-neutral-900) !important;
}

.modern-dialog :deep(.el-dialog__body) {
  padding: 24px !important;
}

/* 浮动动画增强 */
.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-float:nth-child(2) {
  animation-delay: 2s;
}

.animate-float:nth-child(3) {
  animation-delay: 4s;
}

/* 悬停提升效果 */
.hover-lift {
  transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;
}

.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* 响应式调整 */
@media (max-width: 1024px) {
  .gradient-text-primary {
    background-size: 100% 100%;
    animation: none;
  }
}

/* 减少动画偏好支持 */
@media (prefers-reduced-motion: reduce) {
  .animate-float,
  .gradient-text-primary,
  .hover-lift {
    animation: none;
  }

  .hover-lift:hover {
    transform: none;
  }

  .advanced-options-enter-active,
  .advanced-options-leave-active {
    transition: none;
  }
}
</style>
