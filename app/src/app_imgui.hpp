// app/src/app_imgui.hpp
#pragma once

void* app_imgui_creer_contexte();
void app_imgui_detruire_contexte(void* contexte);
void app_imgui_initialiser_sdl3(
    void* fenetre,
    void* rendu
);
void app_imgui_configurer();
void app_imgui_terminer_sdl3();
void app_imgui_nouvelle_image();
void app_imgui_nouvelle_frame();
bool app_imgui_commencer(
    const char* titre
);
void app_imgui_terminer();
void app_imgui_rendre();
void app_imgui_rendre_donnees(void* rendu);
void app_imgui_traiter_evenement(void* evenement);
void app_imgui_texte(const char* texte);
bool app_imgui_bouton(const char* texte);
void app_imgui_preparer_fenetre_menu();
void app_imgui_texte_gras(
    const char* texte
);
void app_imgui_centrer_groupe_menu(
    unsigned int nombre_elements
);