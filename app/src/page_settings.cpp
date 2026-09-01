// app/src/page_settings.cpp
#include "page_settings.hpp"
#include "page_id.hpp"
#include "app_imgui.hpp"

void PageSettings::definirRappel(
    RappelChangementPage rappel,
    void* contexte
) {
    rappelChangement = rappel;
    contexteRappel = contexte;
}

void PageSettings::dessiner() {
    app_imgui_preparer_fenetre_menu();

    if (!app_imgui_commencer("Parametres")) {
        app_imgui_terminer();
        return;
    }

    if (app_imgui_bouton("Retour")) {
        if (rappelChangement != nullptr) {
            rappelChangement(
                contexteRappel,
                static_cast<unsigned int>(
                    PageId::Menu
                )
            );
        }
    }

    app_imgui_terminer();
}