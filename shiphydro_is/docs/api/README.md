# ShipHydro-IS API

主要接口：

- `POST /api/v1/jobs`：提交几何+工况运行任务。
- `GET /api/v1/jobs/{job_id}`：查询任务状态。
- `GET /api/v1/results/{job_id}`：读取阻力等指标。
- `POST /api/v1/drivers/dryrun`：审计外部求解器命令。

启动后端后可在 `http://localhost:8000/docs` 查看完整 OpenAPI 文档。
