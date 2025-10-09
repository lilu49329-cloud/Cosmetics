# Chuyển vào đúng thư mục dự án
$projectPath = "$PSScriptRoot"
Set-Location -Path $projectPath

# Kích hoạt môi trường ảo
& "$projectPath\venv\Scripts\Activate.ps1"

# Cài đặt package
pip install -r requirements.txt

# Chạy migrate
python manage.py migrate

# Chạy server Django
python manage.py runserver
