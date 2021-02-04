## Create Graders Script

Creates the shared grader notebook list by looping through a course list and then calls the
grader-setup-service microservice to create the grader notebook for the course if it doesn't exist.

Execute the steps below to delete stale graders and re create them. The last step restarts the hub so
that graders appear in the drop-down menu.

- Get all grader services (svc) in the namespace:

```bash
kubect get svc -n <namespace>
```

- Copy all grader services from the console

- Paste the list of graders into your preferred text editor notepad. Prepend all lines in the beginning with `"` and end with `",` (note the comma), for example:

```bash
"grader-foo-bar",
"grader-bizz-bazz",
```

- Add the grader list to the `add_graders.py` script within the `graders` array.

- Delete all graders based on regex patters (delimted by pipes with the awk command): 

```bash
kubectl get deployment -n <namespace> --no-headers=true \
  | awk '/grader-0|grader-1/{print $1}' \
  | xargs  kubectl delete -n <namespace> svc,deployment
```

> The `grader-0` and `grader-1` patterns will search for strings that start with grader-0 and grader-1, respectively. Refrain from using just `grader-` since this would delete the `grader-setup-service`!

- Fetch the `grader-setup-service` pod name and then Exec into the `grader-setup-service` pod:

```bash
kubectl get pods -n <namespace>
kubectl exec --stdin --tty grader-setup-service-<id> -n <namespace> -- /bin/bash
```

- Once you have access to the shell prompt, export required environment vars:

```bash
export ORG_NAME=flatiron
export GRADER_SERVICE_NAME=grader-setup-service
export GRADER_SERVICE_PORT=8000
```

- Run the add_graders.py script:

```bash
python add_graders.py
```

- Finally, restart the hub so the graders appear in the hub's services dropdown:

```bash
kubectl rollout restart deployment hub -n <namespace>
```
