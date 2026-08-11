# ใช้ base image แบบ slim เพื่อลด attack surface และขนาด image
FROM python:3.11-slim

# สร้าง working directory
WORKDIR /app

# ติดตั้ง dependencies ก่อน (แยก layer เพื่อใช้ Docker cache ได้ดีขึ้น)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy โค้ดแอปเข้ามา
COPY app/main.py .

# สร้าง non-root user แล้วสลับไปใช้ user นี้แทน root
# นี่คือจุดสำคัญของ DevSecOps: ไม่รัน container ด้วยสิทธิ์ root
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

EXPOSE 5000

CMD ["python", "main.py"]
