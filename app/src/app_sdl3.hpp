// app/src/app_sdl3.hpp
#pragma once

void* app_sdl3_initialiser();
void* app_sdl3_creer_fenetre(
    const char* titre,
    int largeur,
    int hauteur
);
void* app_sdl3_creer_rendu(void* fenetre);
void app_sdl3_demander_fermeture();
void app_sdl3_detruire_rendu(void* rendu);
void app_sdl3_detruire_fenetre(void* fenetre);
bool app_sdl3_traiter_evenements(bool* enCours);
void app_sdl3_definir_couleur_rendu(
    void* rendu,
    unsigned char rouge,
    unsigned char vert,
    unsigned char bleu,
    unsigned char alpha
);
void app_sdl3_effacer_rendu(void* rendu);
void app_sdl3_presenter_rendu(void* rendu);
void app_sdl3_terminer();