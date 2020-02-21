# Kubernetes Authentication

For user authentication, use [OpenID Connect (OIDC)](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#openid-connect-tokens), allowing existing Google email addresses and groups as users
and groups within Kubernetes.

## Kubernetes security components

- Dex as an [Identity Provider (IDP)](https://en.wikipedia.org/wiki/Identity_provider), which acts as an authentication proxy. Dex is an OIDC provider which grants users short-lived, auto-refreshed, [JWT](https://jwt.io/) ID Tokens. These tokens are signed by Dex using the keys in the `keys` table, and can be used to authenticate into the Kubernetes API.
- ouath2_proxy: A web service that protects web pages from unauthorised access

1. kubectl includes `Authorization: Bearer ...` in the request to the apiserver.
2. apiserver fetches signing keys from Dex
3. apiserver validates token signature against signing key
4. apiserver accepts `email` as username and `groups` as groups
5. apiserver performs authorization
6. apiservers returns a response to kubectl

## Emergencies

### Emergency access

If Dex is down, generate emergency temporary credentials from Vault using a KMS key, then create a `kubeconfig` file to access between yourself and the cluster in Terraform. Set your `KUBECONFIG` environment variable to point to the new `kubeconfig` via: `export KUBECONFIG=kubeconfig`. Verify connection via `kubectl cluster-info`.

### Security reset

When the apiserver receives an authentication token, it requests the public keys from Dex to verify the signature of the token. By deleting the existing keys, Dex cannot serve the keys that signed the existing tokens and clients will not be able to validate any existing tokens.

To force all users to re-authenticate:

- Create an emergency certificate into a cluster that hosts Dex.
- Delete the `signingkey` CustomResource.

```bash
kubectl delete signingkeies -n auth openid-connect-keys
kubectl get pods -n auth -l app=dex -o name | xargs -I % sh -c 'kubectl delete -n auth %; sleep 10;'
```

Since these tokens, like certificates, have a finite lifetime the apiserver will then cache the valid token so it does not need to recheck the signature for every request. Therefore, to fully revoke the tokens you will need to restart the `apiserver` on each cluster.

```bash
for p in $( kubectl get pods -n kube-system -l k8s-app=kube-apiserver -o name);
    do ssh core@$(echo $p | sed 's/pod\/kube-apiserver-//' | sed 's/ec2.internal/icelyn.io/') 'docker kill $(docker ps -f name=k8s_kube-apiserver -q)';
done
```
