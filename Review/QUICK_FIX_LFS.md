# 🚀 Guia Rápido: Corrigir Erro Git LFS

## ⚡ Ação Imediata (Fazer AGORA)

### 1️⃣ Faça upload do modelo para GitHub Release

```bash
# Opção A: Via navegador (MAIS FÁCIL)
# 1. Vá para: https://github.com/Mateus-Redivo/FlightOnTime/releases/new
# 2. Tag: v1.0.0
# 3. Title: ML Model v1.0.0
# 4. Arraste: Modelagem/Modelos/modelo_atraso_voos_rf_res.pkl
# 5. Clique em "Publish release"

# Opção B: Via linha de comando
cd d:\FlightOnTime\Modelagem\Modelos
gh release create v1.0.0 modelo_atraso_voos_rf_res.pkl --title "ML Model v1.0.0" --notes "Random Forest model (667 MB)"
```

### 2️⃣ Commit e push as alterações dos workflows

```bash
cd d:\FlightOnTime

# Adiciona os arquivos modificados
git add .github/workflows/tests.yml
git add .github/workflows/docker.yml
git add Modelagem/Modelos/Dockerfile
git add .github/scripts/download-model.sh
git add Modelagem/Modelos/download-model-if-missing.sh
git add .gitignore
git add docs/GIT_LFS_MIGRATION.md

# Commit
git commit -m "fix: migrate ML model from LFS to GitHub Releases

- Download model from release v1.0.0 in workflows
- Update Dockerfile to fetch model if not present
- Add model download scripts
- Ignore *.pkl files in future commits
- Resolve Git LFS budget exceeded error"

# Push
git push origin main
```

### 3️⃣ Verifique se o workflow funciona

Acesse: https://github.com/Mateus-Redivo/FlightOnTime/actions

---

## 🎯 O que foi feito

✅ **Workflows atualizados** - Agora baixam modelo da release v1.0.0  
✅ **Dockerfile modificado** - Busca modelo automaticamente se não existir  
✅ **Scripts criados** - Para download manual do modelo  
✅ **Gitignore atualizado** - Novos `.pkl` não serão commitados  
✅ **Documentação** - Guia completo em `docs/GIT_LFS_MIGRATION.md`

---

## 📦 Teste local (opcional)

```bash
# Baixar modelo manualmente
bash .github/scripts/download-model.sh v1.0.0 Modelagem/Modelos

# Verificar
ls -lh Modelagem/Modelos/*.pkl
# Deve mostrar: modelo_atraso_voos_rf_res.pkl (667 MB)
```

---

## ⚠️ Importante

- **NÃO** commite arquivos `.pkl` no futuro (já está no `.gitignore`)
- **SEMPRE** use GitHub Releases para novos modelos
- **ATUALIZE** a versão nos workflows ao criar nova release

---

## 📚 Próximos passos (futuros)

1. **Remover modelo do Git LFS** (opcional, ver `docs/GIT_LFS_MIGRATION.md`)
2. **Automatizar upload** do modelo em CI/CD de treinamento
3. **Implementar versionamento** semântico para modelos

---

**Status:** ✅ Pronto para usar após o upload da release v1.0.0
