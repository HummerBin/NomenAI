from datetime import timedelta
DB_URI="mysql+aiomysql://root:@127.0.0.1:3306/ainame?charset=utf8mb4"


MAIL_USERNAME="330965340@qq.com"
MAIL_PASSWORD=""
MAIL_FROM ="330965340@qq.com"
MAIL_PORT = "587"
MAIL_SERVER="smtp.qq.com"
MAIL_FROM_NAME="思秋"
MAIL_STARTTLS=True
MAIL_SSL_TLS=False

JWT_SECRET_KEY="aasdsfffasd"
JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=15)
JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30)