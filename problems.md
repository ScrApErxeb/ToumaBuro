# Journal des problèmes techniques - Projet Prestataires

## 1. Fonctionnalité de notation de prestataire (avis)
- **Problème :** La fonctionnalité "Comment noter un prestataire" ne fonctionne pas.
- **Statut :** En panne / à implémenter ou corriger.
- **Détails :**  
  - Route Django configurée : `prestataires/<int:prestataire_id>/avis/`  
  - Frontend React : Erreur `No routes matched location "/prestataires/7avis/"`  
  - Nécessite investigation côté frontend et backend.

## 2. Modification d’un prestataire (login > redirection)
- **Problème :**  
  - Après connexion réussie (tokens JWT reçus et valides), la page redirigée ne s’affiche pas correctement.  
  - Les infos utilisateur/prestataire ne s’affichent pas comme prévu.  
- **Hypothèses :**  
  - Mauvaise gestion de l’ID dans le token (`user_id` vs `prestataire_id`).  
  - Liaison `User` / `Prestataire` pas correctement utilisée dans le frontend.  

## 3. Authentification JWT
- **Statut :** Fonctionnelle, tokens bien reçus et stockés côté frontend.

## 4. Prochaines étapes
- Mettre en pause ces bugs liés au backend/login.  
- Se concentrer sur le peaufinage CSS et l’UX/UI.  
- Revenir aux bugs backend/login dès que possible, ou quand une équipe pourra prendre le relais.

---

*Document généré automatiquement par ChatGPT pour flamme, le 4 juin 2025.*
