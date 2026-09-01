// app/src/page_menu.hpp
#pragma once

typedef void (*RappelChangementPage)(
    void* contexte,
    unsigned int identifiant
);

class PageMenu {
public:
    void dessiner();
    void definirRappel(
        RappelChangementPage rappel,
        void* contexte
    );

private:
    RappelChangementPage rappelChangement = nullptr;
    void* contexteRappel = nullptr;
};