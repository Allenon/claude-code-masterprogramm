# Git Setup Guide - Claude Code Masterprogramm

**Anleitung zum Einrichten des Git-Repositories**

---

## 🎯 Ziel

Ein Git-Repository erstellen für:
- ✅ Versionskontrolle aller Lernmaterialien
- ✅ Backup in der Cloud (GitHub/GitLab)
- ✅ Portfolio-Effekt (optional public)
- ✅ Nachvollziehbare Lernreise

---

## 📋 Voraussetzungen

- [ ] Git installiert (`git --version` im Terminal)
- [ ] GitHub/GitLab Account erstellt
- [ ] SSH-Key eingerichtet (optional, aber empfohlen)

---

## 🚀 Setup-Schritte

### Schritt 1: Repository auf GitHub erstellen

**Option A: Via GitHub Web Interface**
1. Gehe zu https://github.com
2. Klicke auf "New Repository"
3. **Repository Name:** `claude-code-masterprogramm`
4. **Description:** "Mein Weg zum Top-1% Agentic AI Experten"
5. **Visibility:** 
   - Private (empfohlen für Start) ✅
   - Public (für Portfolio später)
6. **Initialize:**
   - ✅ Add a README file
   - ✅ Add .gitignore (Python)
   - ⬜ Add a license (später hinzufügen)
7. Klicke "Create repository"

**Option B: Via GitHub CLI**
```bash
gh repo create claude-code-masterprogramm --private --clone
```

---

### Schritt 2: Repository lokal klonen

```bash
# HTTPS (einfacher)
git clone https://github.com/DEIN_USERNAME/claude-code-masterprogramm.git

# SSH (sicherer, wenn eingerichtet)
git clone git@github.com:DEIN_USERNAME/claude-code-masterprogramm.git

# Navigiere ins Repo
cd claude-code-masterprogramm
```

---

### Schritt 3: Curriculum-Dateien kopieren

```bash
# Erstelle Ordnerstruktur
mkdir -p 00_Curriculum

# Kopiere alle Dateien aus Claude
# (Du musst die Dateien aus /mnt/user-data/outputs/00_Curriculum/ 
#  auf deinen lokalen Rechner kopieren und dann ins Git-Repo)

# Beispiel (wenn Dateien lokal heruntergeladen):
cp ~/Downloads/Gesamtcurriculum.md ./00_Curriculum/
cp ~/Downloads/Fortschritts-Tracker.md ./00_Curriculum/
cp ~/Downloads/Modul-Chat-Template.md ./00_Curriculum/
cp ~/Downloads/Quick-Start.md ./00_Curriculum/
cp ~/Downloads/README.md ./00_Curriculum/
cp ~/Downloads/Visueller-Lernpfad.md ./00_Curriculum/
cp ~/Downloads/Master-Checkliste.md ./00_Curriculum/
cp ~/Downloads/.gitignore ./
```

---

### Schritt 4: README.md für Git-Repo anpassen

```bash
# Ersetze das Standard-README mit dem Git-spezifischen
cp 00_Curriculum/GIT_README.md ./README.md
```

---

### Schritt 5: Initiales Commit

```bash
# Alle Dateien stagen
git add .

# Status überprüfen
git status

# Initiales Commit
git commit -m "Initial commit: Curriculum & Setup komplett

- Gesamtcurriculum mit 12 Modulen erstellt
- Fortschritts-Tracker eingerichtet
- Modul-Chat-Template bereit
- Quick-Start & README dokumentiert
- Visuelle Lernpfad-Diagramme hinzugefügt
- Master-Checkliste für Tracking
- .gitignore konfiguriert

Bereit für Modul 1!"

# Push zu GitHub
git push origin main
```

---

## 🔄 Workflow für Module

### Nach jedem Modul:

```bash
# 1. Neue Dateien vom Modul hinzufügen
git add 01_Modul_Grundlagen/

# 2. Fortschritts-Tracker updaten
git add 00_Curriculum/Fortschritts-Tracker.md

# 3. Commit mit aussagekräftiger Message
git commit -m "feat: Modul 1 abgeschlossen - Agentic AI Fundamentals

Completed:
- Research Agent implementiert
- Tool-Use-Paradigma verstanden
- ReAct Pattern praktisch angewendet
- Modul-Prüfung bestanden (Score: 92%)

Zeit investiert: 3.5 Tage
Schwierigkeit: 2/5

Next: Modul 2 - Claude Code Deep Dive"

# 4. Push zu GitHub
git push origin main
```

---

## 📊 Fortschritt tracken

### Badges im README aktualisieren

**Nach jedem Modul:** Update die Badges in `README.md`:

```markdown
[![Module](https://img.shields.io/badge/Module-1%2F12-yellow)]()
```

wird zu:

```markdown
[![Module](https://img.shields.io/badge/Module-2%2F12-yellow)]()
```

---

## 🌿 Branching-Strategie (Optional, aber empfohlen)

### Für Experimente:

```bash
# Neuer Branch für ein Experiment
git checkout -b experiment/new-pattern

# Arbeite am Experiment
# ...

# Commit im Branch
git commit -m "experiment: Testing hierarchical agent pattern"

# Zurück zu main
git checkout main

# Merge wenn erfolgreich
git merge experiment/new-pattern

# Oder: Branch löschen wenn erfolglos
git branch -d experiment/new-pattern
```

### Empfohlene Branches:

- `main` - Stabile, abgeschlossene Module
- `wip/modul-X` - Work-in-Progress für aktuelles Modul
- `experiment/*` - Experimente
- `refactor/*` - Code-Verbesserungen

---

## 🔧 Git-Konfiguration optimieren

```bash
# Dein Name & Email setzen (falls noch nicht geschehen)
git config --global user.name "Dein Name"
git config --global user.email "deine@email.com"

# Schönere Logs
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# Jetzt kannst du `git lg` für schöne Logs verwenden

# Auto-Stash bei Rebase
git config --global rebase.autoStash true

# Default Branch auf 'main'
git config --global init.defaultBranch main
```

---

## 📝 Commit-Message-Template (Optional)

Erstelle `.gitmessage` im Home-Verzeichnis:

```bash
cat > ~/.gitmessage << 'EOF'
# <type>: <subject>
#
# <body>
#
# <footer>
#
# Types:
# feat: Neue Funktionalität/Modul
# fix: Bugfix
# docs: Dokumentation
# test: Tests
# refactor: Code-Umstrukturierung
# chore: Maintenance
#
# Example:
# feat: Modul 5 abgeschlossen - Multi-Agent Systems
#
# - Autonomous Dev Team implementiert
# - 5 verschiedene Agents orchestriert
# - Message-Queue-Kommunikation
#
# Zeit: 5 Tage, Schwierigkeit: 5/5
EOF

git config --global commit.template ~/.gitmessage
```

---

## 🔒 Secrets Management

**NIEMALS committen:**
- API-Keys
- Passwords
- Access Tokens
- Private Keys

**Verwende stattdessen:**
- `.env` Dateien (in .gitignore!)
- Environment Variables
- Secret Management Services (AWS Secrets Manager, etc.)

**Wenn versehentlich commited:**
```bash
# SOFORT Key rotieren/deaktivieren!
# Dann aus Git-Historie entfernen:
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secrets.json" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (VORSICHT!)
git push origin --force --all
```

---

## 🎯 Best Practices

### ✅ DO:
- Commit häufig mit klaren Messages
- Push nach jedem abgeschlossenen Modul
- Update README.md regelmäßig
- Nutze Branches für Experimente
- Schreibe aussagekräftige Commit-Messages

### ❌ DON'T:
- Secrets committen
- Riesige Binär-Dateien (Videos) committen
- Vage Commit-Messages ("Update", "Fix")
- Direkt auf main pushen ohne Review (bei größeren Changes)
- node_modules/ oder venv/ committen

---

## 📊 Repository-Statistiken tracken

### GitHub Stats nutzen:

```bash
# Zeige Statistiken
git log --shortstat --pretty="%cE" | sed 's/\(.*\)@.*/\1/' | sort | uniq -c | sort -nr
```

### Lokale Stats:

```bash
# Anzahl Commits
git rev-list --count main

# Lines of Code
git ls-files | xargs wc -l
```

---

## 🆘 Troubleshooting

### Problem: "fatal: not a git repository"
```bash
# Lösung: Initialisiere Git
git init
```

### Problem: "Permission denied (publickey)"
```bash
# Lösung: SSH-Key einrichten
ssh-keygen -t ed25519 -C "deine@email.com"
# Key zu GitHub hinzufügen: Settings > SSH Keys
```

### Problem: "Merge conflict"
```bash
# Lösung: Manuell auflösen
# 1. Öffne die Datei mit Konflikt
# 2. Suche nach <<<<<<< HEAD
# 3. Entscheide welche Version behalten
# 4. Entferne Konflikt-Marker
# 5. git add <datei>
# 6. git commit
```

### Problem: "Versehentlich falsches commited"
```bash
# Lösung: Letzten Commit rückgängig (lokal)
git reset --soft HEAD~1

# Oder: Letzten Commit ändern
git commit --amend
```

---

## 🎓 Git-Learning-Ressourcen

- **Interactive:** https://learngitbranching.js.org/
- **Cheat Sheet:** https://education.github.com/git-cheat-sheet-education.pdf
- **Pro Git Book:** https://git-scm.com/book/en/v2

---

## ✅ Setup-Checkliste

- [ ] Repository auf GitHub erstellt
- [ ] Lokal geklont
- [ ] Curriculum-Dateien kopiert
- [ ] .gitignore konfiguriert
- [ ] README.md angepasst
- [ ] Initiales Commit gemacht
- [ ] Zu GitHub gepusht
- [ ] Repository-Link gespeichert
- [ ] Git-Konfiguration optimiert
- [ ] Bereit für Modul 1!

---

**Geschafft! Dein Git-Repository ist bereit! 🎉**

**Nächster Schritt:**  
→ Starte mit Modul 1: Agentic AI Fundamentals

---

_Bei Fragen: Zurück zum Master-Chat in Claude_
