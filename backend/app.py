from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# 配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

# 基础路由
@app.route('/')
def index():
    return jsonify({'message': '教务系统API服务运行中'})

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

# 企业微信认证
@app.route('/api/auth/wework')
def wework_auth():
    code = request.args.get('code')
    # 这里调用企业微信API获取用户信息
    return jsonify({'code': 0, 'message': '认证成功'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)