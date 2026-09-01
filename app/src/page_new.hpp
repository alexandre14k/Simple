// app/src/page_new.hpp
#pragma once

typedef void (*RappelChangementPage)(
    void* contexte,
    unsigned int identifiant
);

class PageNew {
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