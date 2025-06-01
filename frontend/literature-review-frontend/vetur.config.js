// Vetur 配置文件 - 解决 Vetur 找不到配置文件的问题
module.exports = {
  // 项目设置
  settings: {
    "vetur.useWorkspaceDependencies": true,
    "vetur.experimental.templateInterpolationService": true
  },
  
  // 项目路径
  projects: [
    {
      // 项目根目录
      root: './',
      // package.json 路径
      package: './package.json',
      // tsconfig.json 路径
      tsconfig: './tsconfig.json',
      // 全局组件路径
      globalComponents: [
        './src/components/**/*.vue'
      ]
    }
  ]
}
