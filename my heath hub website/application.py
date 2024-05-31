from flask import Flask, render_template, request
import paramiko

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect():
    server_address = request.form['server_address']
    private_key_path = request.form['private_key_path']
    
    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_address, username='ubuntu', key_filename=private_key_path)
    
    # Perform actions on the server (e.g., execute commands)
    stdin, stdout, stderr = ssh.exec_command('ls -l')
    output = stdout.read().decode('utf-8')
    
    ssh.close()
    
    return render_template('result.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
