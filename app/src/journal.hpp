// app/src/journal.hpp
#pragma once

class Journal {
public:
    void consigner(const char* message);

private:
    void retenir(
        const char* message
    );

    void formaterHorodatage(
        char* tampon,
        unsigned int taille
    );

    bool journal_actif = false;
};