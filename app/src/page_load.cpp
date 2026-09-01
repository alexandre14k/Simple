// app/src/page_load.cpp
#include "page_load.hpp"
#include "page_id.hpp"
#include "app_imgui.hpp"

void PageLoad::definirRappel(
    RappelChangementPage rappel,
    void* contexte
) {
    rappelChangement = rappel;
    contexteRappel = contexte;
}

void PageLoad::dessiner() {
    app_imgui_preparer_fenetre_menu();

    if (!app_imgui_commencer("Charger")) {
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