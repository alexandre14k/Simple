// app/src/gui.cpp
#include "gui.hpp"
#include "app_imgui.hpp"
#include "app_sdl3.hpp"
#include "app_theme.hpp"
#include "journal.hpp"
#include "page_id.hpp"
#include "page_load.hpp"
#include "page_menu.hpp"
#include "page_new.hpp"
#include "page_settings.hpp"

InterfaceGraphique::InterfaceGraphique()
    : fenetre(nullptr),
      rendu(nullptr),
      contexteImgui(nullptr),
      estInitialise(false),
      journal(nullptr),
      pageMenu(nullptr),
      pageNew(nullptr),
      pageLoad(nullptr),
      pageSettings(nullptr),
      pageActive(PageId::Menu) {
}

InterfaceGraphique::~InterfaceGraphique() {
    nettoyer();
}

void InterfaceGraphique::rappelPageStatique(
    void* contexte,
    unsigned int identifiant
) {
    InterfaceGraphique* interfaceGraphique =
        static_cast<InterfaceGraphique*>(contexte);

    interfaceGraphique->changerPage(
        static_cast<PageId>(identifiant)
    );
}

bool InterfaceGraphique::initialiser() {
    if (app_sdl3_initialiser() == nullptr) {
        return false;
    }

    fenetre = app_sdl3_creer_fenetre(
        "app",
        480,
        320
    );

    if (fenetre == nullptr) {
        app_sdl3_terminer();
        return false;
    }

    rendu = app_sdl3_creer_rendu(
        fenetre
    );

    if (rendu == nullptr) {
        app_sdl3_detruire_fenetre(fenetre);
        fenetre = nullptr;
        app_sdl3_terminer();
        return false;
    }

    contexteImgui =
        app_imgui_creer_contexte();

    if (contexteImgui == nullptr) {
        app_sdl3_detruire_rendu(rendu);
        app_sdl3_detruire_fenetre(fenetre);
        rendu = nullptr;
        fenetre = nullptr;
        app_sdl3_terminer();
        return false;
    }

    app_imgui_initialiser_sdl3(
        fenetre,
        rendu
    );

    app_imgui_configurer();

    journal = new Journal();
    pageMenu = new PageMenu();
    pageNew = new PageNew();
    pageLoad = new PageLoad();
    pageSettings = new PageSettings();

    pageMenu->definirRappel(
        rappelPageStatique,
        this
    );

    pageNew->definirRappel(
        rappelPageStatique,
        this
    );

    pageLoad->definirRappel(
        rappelPageStatique,
        this
    );

    pageSettings->definirRappel(
        rappelPageStatique,
        this
    );

    journal->consigner(
        "demarrage application"
    );

    estInitialise = true;
    return true;
}

void InterfaceGraphique::nettoyer() {
    delete pageMenu;
    delete pageNew;
    delete pageLoad;
    delete pageSettings;

    pageMenu = nullptr;
    pageNew = nullptr;
    pageLoad = nullptr;
    pageSettings = nullptr;

    if (journal != nullptr) {
        journal->consigner(
            "fermeture application"
        );

        delete journal;
        journal = nullptr;
    }

    if (!estInitialise) {
        return;
    }

    app_imgui_terminer_sdl3();

    app_imgui_detruire_contexte(
        contexteImgui
    );

    contexteImgui = nullptr;

    app_sdl3_detruire_rendu(rendu);
    app_sdl3_detruire_fenetre(fenetre);

    rendu = nullptr;
    fenetre = nullptr;

    app_sdl3_terminer();

    estInitialise = false;
}

void InterfaceGraphique::traiterEvenements(
    bool* enCours
) {
    app_sdl3_traiter_evenements(
        enCours
    );
}

void InterfaceGraphique::dessinerPageActive() {
    switch (pageActive) {
        case PageId::Menu:
            pageMenu->dessiner();
            break;

        case PageId::New:
            pageNew->dessiner();
            break;

        case PageId::Load:
            pageLoad->dessiner();
            break;

        case PageId::Settings:
            pageSettings->dessiner();
            break;

        case PageId::Quit:
            break;
    }
}

void InterfaceGraphique::changerPage(
    PageId identifiant
) {
    if (identifiant == PageId::Quit) {
        journal->consigner(
            "demande fermeture"
        );

        app_sdl3_demander_fermeture();

        return;
    }

    pageActive = identifiant;

    journal->consigner(
        "changement page"
    );
}

void InterfaceGraphique::dessinerImage() {
    app_imgui_nouvelle_image();
    app_imgui_nouvelle_frame();

    app_theme_appliquer_echelle(
        fenetre
    );

    dessinerPageActive();

    app_imgui_rendre();

    app_sdl3_definir_couleur_rendu(
        rendu,
        20,
        20,
        20,
        255
    );

    app_sdl3_effacer_rendu(
        rendu
    );

    app_imgui_rendre_donnees(
        rendu
    );

    app_sdl3_presenter_rendu(
        rendu
    );
}

void InterfaceGraphique::bouclePrincipale() {
    bool enCours = true;

    while (enCours) {
        traiterEvenements(
            &enCours
        );

        dessinerImage();
    }
}

int InterfaceGraphique::executer() {
    if (!initialiser()) {
        return 1;
    }

    bouclePrincipale();
    nettoyer();

    return 0;
}