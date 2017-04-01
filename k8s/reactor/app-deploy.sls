{%  set app = data['data']['app'] %}
{%  set version = data['data']['version'] %}

k8s-deploy:
  local.cmd.run:
    - tgt: 'k8s-deployer'
    - expr_form: grain
    - arg:
      - 'kubectl -n flask set image deployment/flask-deployment {{ app }}=pythonrocks/{{ app }}:{{ version }}'
