# ShipHydro-IS

ShipHydro-IS 是一个面向船舶流体设计与工业软件协同的最小可运行演示系统，包含 Python FastAPI 后端、React + Three.js 前端、mock CFD 求解器与容器化部署脚本。

## 目录结构

```
shiphydro_is/
  backend/
  frontend/
  deploy/
  docs/
  examples/
```

## 快速开始

1. 初始化数据库并运行后端：

```bash
cd shiphydro_is/backend
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

2. 启动前端：

```bash
cd ../frontend
npm install
npm run dev
```

3. 使用 `make demo` 运行端到端示例（mock 求解）：

```bash
make demo
```

## Demo 工作流

1. 解析 `examples/geometries/bulbous_bow.yaml` 生成 STL。
2. 构建最小 OpenFOAM case（mock）。
3. 运行 `CFDSolverMock` 生成阻力数据并入库。
4. 前端监控页面可看到阻力 KPI 与收敛曲线。

## 依赖与 Mock

- 几何与 CFD 默认使用 mock 组件，无需外部许可证。
- 数据库存储使用 SQLite，可配置 PostgreSQL。
- MLflow、MinIO、Redis 等可选组件在本演示中通过本地 mock 替代。
