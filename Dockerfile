
#TODO: 复制的模板, 如何配置

# 使用官方 Python 3.10 镜像作为基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制应用代码到容器中
COPY . /app

# 安装应用依赖
RUN git clone ???
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用的端口（如果需要）
EXPOSE 6660

# 设置应用的入口命令
CMD [ "python", "app.py" ]