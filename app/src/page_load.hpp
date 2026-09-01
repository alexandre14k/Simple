// app/src/page_load.hpp
#pragma once

typedef void (*RappelChangementPage)(
    void* contexte,
    unsigned int identifiant
);

class PageLoad {
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