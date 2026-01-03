module.exports = {
  apps: [{
    name: 'wgs-slicer',
    script: 'streamlit',
    args: 'run WGS_Slicer_v2.py --server.port=8501 --server.address=0.0.0.0',
    interpreter: 'python3',
    cwd: './',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
};

