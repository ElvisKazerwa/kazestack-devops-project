# Troubleshooting Guide

## Common Issues

### Pod fails to start

Check logs: `kubectl logs <pod-name>`
Common causes:

- Image not found in registry
- Insufficient resources
- Configuration errors

### Deployment stuck in pending

- Check resource availability: `kubectl describe pod <pod-name>`
- Verify node affinity rules
- Check resource quotas

### Connection timeout to service

- Verify service is running: `kubectl get svc`
- Check ingress configuration
- Verify network policies

## Debug Logs

```bash
# View pod logs
kubectl logs <pod-name>

# View previous pod logs (if crashed)
kubectl logs <pod-name> --previous

# Get detailed pod information
kubectl describe pod <pod-name>

# Check deployment status
kubectl rollout status deployment/kazestack-devops-project
```

## Support

For issues or questions, refer to:

- Kubernetes docs: https://kubernetes.io/docs/
- Azure AKS docs: https://docs.microsoft.com/azure/aks/
- Terraform docs: https://www.terraform.io/docs/
