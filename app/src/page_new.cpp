// app/src/page_new.cpp
#include "page_new.hpp"
#include "page_id.hpp"
#include "app_imgui.hpp"

void PageNew::definirRappel(
    RappelChangementPage rappel,
    void* contexte
) {
    rappelChangement = rappel;
    contexteRappel = contexte;
}

void PageNew::dessiner() {
    app_imgui_preparer_fenetre_menu();

    if (!app_imgui_commencer("Nouveau")) {
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