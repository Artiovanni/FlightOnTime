# Solução para Git LFS Budget Exceeded

## 🔴 Problema

O repositório excedeu o limite gratuito do Git LFS (Large File Storage) do GitHub devido ao modelo ML de 667 MB (`modelo_atraso_voos_rf_res.pkl`).

## ✅ Solução Implementada

Migração do modelo de **Git LFS** para **GitHub Releases**.

### Vantagens

- ✅ Sem limites de largura de banda para downloads públicos de releases
- ✅ Versionamento claro do modelo
- ✅ Workflows do GitHub Actions funcionam normalmente
- ✅ Downloads sob demanda (não clona com o repositório)

---

## 📦 Como Fazer Upload do Modelo (Primeira Vez)

### Opção 1: Via GitHub Web Interface (Recomendado)

1. Acesse: <https://github.com/Mateus-Redivo/FlightOnTime/releases/new>
2. Preencha:
   - **Tag version:** `v1.0.0`
   - **Release title:** `ML Model v1.0.0`
   - **Description:** `Random Forest model for flight delay prediction (667 MB)`
3. Arraste o arquivo `modelo_atraso_voos_rf_res.pkl` para a seção "Attach binaries"
4. Clique em **Publish release**

### Opção 2: Via GitHub CLI

```bash
# Instale o GitHub CLI: https://cli.github.com/

# Autentique
gh auth login

# Crie a release com o modelo
cd Modelagem/Modelos
gh release create v1.0.0 \
  modelo_atraso_voos_rf_res.pkl \
  --title "ML Model v1.0.0" \
  --notes "Random Forest model for flight delay prediction"
```

---

## 🔄 Como Atualizar o Modelo

Quando treinar uma nova versão do modelo:

```bash
# 1. Crie uma nova release com versão incrementada
gh release create v1.1.0 \
  modelo_atraso_voos_rf_res.pkl \
  --title "ML Model v1.1.0" \
  --notes "Descrição das melhorias"

# 2. Atualize a versão nos workflows
# Edite .github/workflows/tests.yml e .github/workflows/docker.yml
# Substitua v1.0.0 por v1.1.0 nas URLs de download
```

---

## 🏗️ Como os Workflows Funcionam Agora

### 1. GitHub Actions

Os workflows baixam automaticamente o modelo da release:

```yaml
- name: Download ML model from release
  run: |
    curl -L -o Modelagem/Modelos/modelo_atraso_voos_rf_res.pkl \
      https://github.com/Mateus-Redivo/FlightOnTime/releases/download/v1.0.0/modelo_atraso_voos_rf_res.pkl
```

### 2. Docker Build Local

O Dockerfile tenta copiar o modelo local primeiro. Se não existir, baixa da release:

```bash
# Para build local com modelo existente
docker build -t ml-model:latest Modelagem/Modelos/

# Para build sem modelo (baixa automaticamente)
docker build -t ml-model:latest Modelagem/Modelos/
```

### 3. Download Manual

Use o script auxiliar:

```bash
# Baixa o modelo para desenvolvimento local
bash .github/scripts/download-model.sh v1.0.0 Modelagem/Modelos
```

---

## 🧹 Limpeza do Git LFS (Opcional)

Para remover o modelo do histórico do Git LFS e economizar espaço:

```bash
# ATENÇÃO: Isso reescreve o histórico do Git!
# Faça backup antes de executar

# 1. Remove o tracking do LFS
git lfs untrack "*.pkl"
rm .gitattributes

# 2. Remove o arquivo do índice
git rm --cached Modelagem/Modelos/modelo_atraso_voos_rf_res.pkl

# 3. Adiciona ao .gitignore
echo "*.pkl" >> .gitignore
git add .gitignore

# 4. Commit
git commit -m "chore: migrate model from LFS to GitHub Releases"

# 5. Limpa o histórico LFS (opcional, avançado)
git filter-repo --path Modelagem/Modelos/modelo_atraso_voos_rf_res.pkl --invert-paths
```

---

## 📋 Checklist de Migração

- [ ] Fazer upload do modelo para GitHub Release v1.0.0
- [ ] Verificar se a URL de download funciona
- [ ] Testar workflow do GitHub Actions
- [ ] Atualizar documentação do projeto
- [ ] (Opcional) Remover modelo do Git LFS
- [ ] Atualizar `.gitignore` para ignorar `*.pkl` em futuros commits

---

## 🆘 Troubleshooting

### Erro: "Release v1.0.0 not found"

- Certifique-se de ter criado a release no GitHub
- Verifique se o arquivo foi anexado corretamente

### Erro: "curl: Connection timeout"

- Aumente o timeout: `--max-time 900`
- Tente novamente mais tarde

### Modelo não carrega no Docker

- Verifique os logs: `docker logs <container-id>`
- Confirme que o arquivo foi baixado: `docker exec <container-id> ls -lh *.pkl`

---

## 📚 Referências

- [GitHub Releases Documentation](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Git LFS Billing](https://docs.github.com/en/billing/managing-billing-for-git-large-file-storage)
- [GitHub CLI Releases](https://cli.github.com/manual/gh_release_create)
