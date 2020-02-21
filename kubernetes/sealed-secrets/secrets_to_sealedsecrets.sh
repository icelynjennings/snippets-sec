secrets=$(kubectl get secrets --all-namespaces | awk 'NR>2 {print $1,$2}' | grep -v token | grep -v istio)

context=$(kubectl config current-context)

while read -r i
do
  ns=$(echo $i | awk '{print $1}')
  name=$(echo $i | awk '{print $2}')
  mkdir -p ./sealed/${context}/${ns}
  kubectl get secret -n ${ns} ${name} -o yaml > tmp_${context}_${ns}_${name}.yaml
  kubeseal --format yaml <tmp_${context}_${ns}_${name}.yaml > ./sealed/${context}/${ns}/${name}.yaml
  rm tmp_${context}_${ns}_${name}.yaml
  printf "sealed %s %s\n" "${ns}" "${name}"
done <<< "$secrets"
