module.exports = {
  /**
   * Application configuration section
   * http://pm2.keymetrics.io/docs/usage/application-declaration/
   */
  apps: [

    // First application
    {
      name: "DynamicProxyIP",
      max_memory_restart: "1024M",
      log_date_format: "YYYY-MM-DD HH:mm:ss SSS",
      script: "start.py",
      out_file: "/var/log/DynamicProxyIP/app.log",
      error_file: "/var/log/DynamicProxyIP/err.log",
      port: "6800",
      env: {
        COMMON_VARIABLE: 'true'
      },
      env_production: {
        NODE_ENV: 'production'
      }
    },
  ],

  /**
   * Deployment section
   * http://pm2.keymetrics.io/docs/usage/deployment/
   */
  deploy: {
    production: {
      user: 'root',
      host: '116.62.195.14',
      ref: 'origin/master',
      repo: 'git@github.com:sqzxcv/DynamicProxyIP.git',
      path: '/var/www/DynamicProxyIP',
      // "post-deploy": 'git pull && workon scrapyd_py3.6.1 && npm install && pm2 reload scrapyd -x --interpreter /root/Envs/scrapyd_py3.6.1/bin/python'
      "post-deploy": './start.sh'
    }
  }
};
