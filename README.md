# 智能家居控制系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D16.0.0-brightgreen)](https://nodejs.org/)
[![NPM Version](https://img.shields.io/badge/npm-%3E%3D8.0.0-red)](https://www.npmjs.com/)

## 项目简介

智能家居控制系统是一个集成化的IoT平台，支持多种智能设备的统一管理和控制。系统提供设备连接、场景自动化、能源监控、安全监控等功能，为用户打造智能、安全、节能的家居环境。

## 主要功能

- 🏠 **设备管理** - 支持智能照明、温控、安防、门锁等多种设备
- 🤖 **场景自动化** - 创建自定义场景和定时控制
- ⚡ **能源监控** - 实时能耗显示和历史数据分析
- �� **安全监控** - 实时监控画面和移动侦测报警
- �� **远程控制** - 支持iOS/Android APP远程访问
- 🌐 **多协议支持** - 支持WiFi、Zigbee、Z-Wave等协议

## 技术栈

- **后端**: Node.js + Express + Socket.io
- **数据库**: MongoDB + Mongoose
- **通信**: MQTT + WebSocket
- **安全**: JWT + bcryptjs + Helmet
- **监控**: Winston日志 + 自定义监控
- **文档**: 自动化用户手册生成

## 快速开始

### 环境要求

- Node.js >= 16.0.0
- NPM >= 8.0.0
- MongoDB >= 4.4
- MQTT Broker (可选)

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/smc1040937705/smart-home-control-system.git
   cd smart-home-control-system
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，配置数据库连接等信息
   ```

4. **启动服务**
   ```bash
   # 开发模式
   npm run dev
   
   # 生产模式
   npm start
   ```

### 用户手册生成

系统支持自动生成用户手册：

```bash
# 生成用户手册
npm run generate-manual

# 验证手册格式
npm run validate-manual
```
