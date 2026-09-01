// app/src/page_menu.cpp
#include "page_menu.hpp"
#include "page_id.hpp"
#include "app_imgui.hpp"
#include "app_theme.hpp"

void PageMenu::definirRappel(
    RappelChangementPage rappel,
    void* contexte
) {
    rappelChangement = rappel;
    contexteRappel = contexte;
}

void PageMenu::dessiner() {
    app_imgui_preparer_fenetre_menu();

    if (!app_imgui_commencer("Menu")) {
        app_imgui_terminer();
        return;
    }

    app_imgui_centrer_groupe_menu(4);

    if (app_imgui_bouton("Nouveau")) {
        if (rappelChangement != nullptr) {
            rappelChangement(
                contexteRappel,
                static_cast<unsigned int>(
                    PageId::New
                )
            );
        }
    }

    if (app_imgui_bouton("Charger")) {
        if (rappelChangement != nullptr) {
            rappelChangement(
                contexteRappel,
                static_cast<unsigned int>(
                    PageId::Load
                )
            );
        }
    }

    if (app_imgui_bouton("Parametres")) {
        if (rappelChangement != nullptr) {
            rappelChangement(
                contexteRappel,
                static_cast<unsigned int>(
                    PageId::Settings
                )
            );
        }
    }

    if (app_imgui_bouton("Quitter")) {
        if (rappelChangement != nullptr) {
            rappelChangement(
                contexteRappel,
                static_cast<unsigned int>(
                    PageId::Quit
                )
            );
        }
    }

    app_imgui_terminer();
}