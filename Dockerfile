# 使用官方 Python 3.11 精简版作为基础镜像
FROM python:3.11-slim

# 设置工作目录（容器里的项目文件夹）
WORKDIR /app

# 把当前文件夹的所有文件复制到容器的 /app 目录
COPY . /app

# 安装依赖
RUN pip install -r requirements.txt

# 告诉别人这个容器会监听哪个端口
EXPOSE 8000

# 容器启动时自动执行的命令
CMD ["uvicorn", "wangba_api:app", "--host", "0.0.0.0", "--port", "8000"]