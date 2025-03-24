suivi de la consommation de chaque opérateur

# Processus d'intégration d'un flux de données

## Contexte

L'intégration des données dans Qualicharge s'appuie sur un processus rigoureux pour garantir un haut niveau de qualité des données.

Les objectifs recherchés par cette intégration sont :

- d'obtenir une image fidèle et actualisée des infrastructure de recharge déployées,
- de suivre précisément la consommation de chaque opérateur (calcul des certificats TIRUERT alloués)
- de mettre à disposition en temps réel les données d'usage sur le point d’accès national transport.data.gouv.fr

Le processus mis en place s'appuie sur une définition précise des données attendues (structure de données) ainsi que sur un ensemble de contrôles des flux de données mis en place par chaque opérateur.

## Structure des données

### Principales notions

La structure des données de Qualicharge s'appuie sur les notions définies par la réglementation AFIR (Alternative Fuels Infrastructure - [règlement UE 2023/1804 du 13/09/2023](https://eur-lex.europa.eu/eli/reg/2023/1804/oj)), en particulier les notions de point de recharge, station de recharge et parc de recharge :

"*point de recharge: une interface fixe ou mobile, sur réseau ou hors réseau, qui permet de transférer de l’électricité vers un véhicule électrique et qui, bien qu’elle puisse être équipée d’un ou de plusieurs connecteurs pour prendre en charge différents types de connecteurs, n’est capable de recharger qu’un seul véhicule électrique à la fois, à l’exclusion des dispositifs d’une puissance de sortie inférieure ou égale à 3,7 kW dont la fonction principale n’est pas de recharger des véhicules électriques*"

"*station de recharge: une installation physique en un lieu spécifique, composée d’un ou de plusieurs points de recharge*"

"*parc de recharge: une ou plusieurs stations de recharge en un lieu spécifique*"

La notion de point de recharge est explicite dans sa formulation. Les notions de stations de recharge et de parcs de recharge nécessitent néanmoins une explication complémentaire :

- la station de recharge est définie dans la règlementation AFIR au travers des informations qui lui sont associées. On peut ainsi la définir comme étant un regroupement de points de recharge partageant les mêmes informations de gestion et de pilotage. Par exemple :
  - une localisation géographique,
  - un rattachement administratif (propriétaire, opérateur, aménageur),
  - des conditions tarifaires,
  - des propriétés (accessibilité, horaires)

Ainsi, par exemple, deux points de recharge ne partageant pas la même localisation ne pourront être associés à la même station.

- le parc de recharge ne fait référence à aucune activité de gestion mais est associé exclusivement aux exigences règlementaire portant sur un lieu. Ainsi un parc regroupe par exemple toutes les stations d'une aire de service autoroutière ou bien d'une gare ou d'un aéroport. Il reflète en ce sens le besoin usager de recharge en un lieu donné.

Dans le cadre de Qualicharge la notion de station est conforme à la notion présentée dans la règlementation AFIR. La notion de parc de recharge n'est pas utilisée.

### Schéma de données IRVE

Les données des infrastructures de recharge des véhicules électriques font déjà l'objet d'une consolidation au niveau de *transport.data.gouv.fr*. Cette consolidation s'appuie sur un [schéma de données détaillé](https://doc.transport.data.gouv.fr/type-donnees/infrastructures-de-recharge-de-vehicules-electriques-irve).

Les données Qualicharge respectent le schéma de données IRVE en le complétant (par exemple avec la notion de session) ou en le renforçant (des données facultatives peuvent devenir obligatoire).

### Modèle de données Qualicharge

Outre les stations et points de recharge, le modèle Qualicharge s'appuie sur les entités suivante :

- aménageur : entité publique ou privée propriétaire des infrastructures (définition du schéma de données),
- opérateur : personne qui exploite l'infrastructure de recharge pour le compte d'un aménageur dans le cadre d'un contrat ou pour son propre compte s'il est l'aménageur (définition du schéma de données)
- enseigne : nom commercial du réseau (définition du schéma de données)
- localisation : localisation géographique et administative d'une station
- operational unit (unité d'exploitation): réseau d’infrastructures de recharge exploité par un unique opérateur d’infrastructure de recharge et accessible à l’itinérance par une seule connexion informatique (définition AFIREV)
- status : état instantané d'un point de recharge (occupation, fonctionnement)
- session : session de recharge d'un véhicule (durée, énergie)

Il est présenté ci-dessous sous la forme "entité-association". Les attributs liés à ce modèle sont explicités dans le schéma de données (à l'exception des attributs liés aux sessions)

```{index} Modèle de données Qualicharge
```

```{mermaid}
erDiagram
    AMENAGEUR ||..|{ STATION : amenage
    AMENAGEUR {
        string nom_amenageur PK "M"
        string siren_amenageur "M"
        string contact_amenageur "M"
    }
    OPERATEUR ||..|{ STATION : "exploite pour le compte de l enseigne"
    OPERATEUR {
        string nom_operateur PK "M"
        string contact_operateur "M"
        string telephone_operateur "M"
    }
    ENSEIGNE ||..|{ STATION : "heberge"
    ENSEIGNE {
        string nom_enseigne PK "M" 
    }
    STATION {
        string  id_station_itinerance PK "M"
        string  nom_station "M"
        enum    implantation_station "M"
        integer nbre_pdc "M"
        string  condition_acces "M"
        string  horaires "M"
        boolean station_deux_roues "M"
        date    date_maj "M"
        string  num_pdl "M"
        string  id_station_local
        enum    raccordement
        date    date_mise_en_service 
    }
    LOCALISATION ||--|{ STATION : "localise"
    LOCALISATION {
       array   coordonneesXY PK "M"
       string  adresse_station "M"
       string  code_insee_commune "M"
    }
    STATION ||--|{ POINT_DE_CHARGE : regroupe
    POINT_DE_CHARGE {
        string id_pdc_itinerance PK "M"
        number puissance_nominale "M"
        boolean prise_type_ef "M"
        boolean prise_type_2 "M" 
        boolean prise_type_combo_ccs "M"
        boolean prise_type_chademo "M"
        boolean prise_type_autre "M"
        boolean paiement_acte "M"
        boolean reservation "M"
        enum    accessibilite_pmr "M"
        string  restriction_gabarit "M"
        string  id_pdc_local
        boolean gratuit
        boolean paiement_cb
        boolean paiement_autre
        string  tarification
        string  observations
        boolean cable_t2_attache
    }
    OPERATIONAL_UNIT ||--|{ STATION : "relationship"
    OPERATIONAL_UNIT {
        string code PK "M"
        string name "M"
        enum type "M"
    }
    POINT_DE_CHARGE ||--|{ SESSION : "a pour session"
    SESSION {
        datetime start "M"
        datetime end "M"
        number energy "M"
    }
    POINT_DE_CHARGE ||--|{ STATUS : "a pour status"
    STATUS {
        datetime horodatage "M"
        enum     etat_pdc "M"
        enum     occupation_pdc "M"
        enum     etat_prise_type_2
        enum     etat_prise_type_combo_ccs
        enum     etat_prise_type_chademo
        enum     etat_prise_type_ef
    }
```

*figure 1 :* *Modele qualicharge - v0.5.0*

Notation :

- PK: Indique un attribut identifiant de façon unique une entité (ex. "ccordonneesXY" identifie de façon unique une localisation)
- M : Indique un attribut devant être renseigné obligatoirement
- relation entre entités : Les relations indiquées sont des relations 1-n exprimant le fait que dans un sens, une entité A peut être associée à plusieurs entités B mais que dans l'autre sens une entité B peut etre associée à une seule entatité A (ex. une station est associée à une seule location mais une location peut être associée à plusieurs stations).

Conséquences :

- attributs : chaque attribut est associé à une entité par une relation 1-n. Lorsque l'entité est définie par un attribut principal cela signifie qu'on ne peut avoir deux valeurs d'attribut différentes associé à un même attribut principal. Par exemple :
  - une même "coordonneesXY" ne peut être associée à deux "adresse_station" différentes,
  - 

## Compatibilité indicateurs

Le modèle contient l'ensemble des informations permettant de générer les indicateurs à l'exception des informations suivantes :

- état activé ou désactivé d'un point de recharge (ou d'une station): Cette information est nécessaire pour ne pas fausser les indicateurs (ne pas tenir compte des points de recharge désactivés). Des points restent à clarifier concernant la propagation de l'état (ex. est-ce que lorsque tous les pdc d'une station sont désactivés, la station l'est aussi  - idem pour les localisations associées) et la réactivation (est-ce autorisé ?).
- identification de l'opérateur: La seule information obligatoire concernant l'opérateur est une adresse email (le nom de l'opérateur est optionnel). Ce point rejoint un point évoqué dans le chapitre suivant.
- identification de l'aménageur: L'aménageur n'est pas identifié explicitement (toutes les informations liées à l'aménageur sont optionnelles)Ce point rejoint un point évoqué dans le chapitre suivant.
- identification de la localisation: Aucun identifiant n'est défini pour la localisation. L'information principale qui pourrait faire office d'identifiant est la coordonnée géographique.
- site d'implantation: Les types d'implantation définis ne permettent pas de restituer la nature du site telle qu'elle est restituée par l'AVERE (ex. commerce, entreprise)
- puissance: La puissance est actuellement identifiée par une valeur. Une classification par niveau de puissance permettrait des analyses par gamme de puissance. Cette information est gérée actuellement de façon dynamique ce qui semble être suffisant.
- type d'alimentation AC/DC: Cette information est souhaitable. Elle est gérée dynamiquement actuellement. Est-ce suffisant ?
- Type de session: Cette information permettrait d'identifier par exemple les charges partielles ou interrompues. Les sessions non réussies sont calculées dynamiquement, ce serait peut-être intéressant en terme de performance d'avoir cette information de façon statique.
- tarification: Cette information est souhaitable (présente dans les indicateurs AVERE)
- qualité de service: le taux d'occupation ou la disponibilité d'un point de charge nécessite de disposer du temps passé dans chaque état (voir [état des points de recharge](./etats.md)). Cette information est présente pour les sessions (table 'session') mais pas pour les périodes d'indisponibilité (pannes ou arrêt). La aussi, pour des raisons de performance, il peut être utile de reconstruire et de stocker les différents états (dans ce cas ça peut être géré en dehors de la base de données actuelle)

## Autres besoins d'évolutions du modèle de données

- besoin d'identifier de façon unique le "responsable initial" du PDC correctement, et d'avoir également l'email de contact fiable du producteur de la donnée (besoin : pouvoir le notifier de façon fiable en automatique, pour scaler le dispositif d'un point de vue gestion chez nous)
- énorme point d'attention concernant la "productibilité" (fait d'être produit plus ou moins facilement) des champs. En effet vu la variété des acteurs, et l'historique, on va fragmenter la qualité de la base consolidée si on ne prête pas attention suffisante à ça (certains pourront produire, d'autres pas si facilement), voire, perdre des PDC (situation qui se produisait en v2 initialement, qui nous a amené à rendre optionnels certains champs)
- sur les formats des attributs, on gagnera à homogénéiser (ou à transformer à la volée quand on consolide si ça peut se faire simplement) et resserrer la vis
- Une autre option pour simplifier pourrait être de sortir les attributs liés aux opérateurs et aux aménageurs (données quasi-fixes qui sont plus associées à un profil admin et qui pourraient être gérées séparément). Il n'y aurait dans ce cas qu'un seul attribut `id_operateur` et `id_amenageur` à associer aux stations. Ca permettrait également de faciliter les transferts de responsabilité de stations d'un opérateur à l'autre (sinon, c'est plus compliqué à gérér).
- le point de livraison nécessitera peut-être des informations complémentaires, une entité dédiée serait alors à envisager ?

## Règlementation AFIR

Premier décodage de la règlementation (AFIR) des données statiques et dynamiques :

- [règlement UE 2023/1804 du 13/09/2023](https://eur-lex.europa.eu/eli/reg/2023/1804/oj)
- [règlement délégué](https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14347-Donnees-sur-linfrastructure-pour-carburants-alternatifs-types-de-donnees-supplementaires_fr) modifiant l’article 20, paragraphe 2 (fin décembre)
- annexe de spécification (version Nicolas du 13/01/25) :
  - Tables A et B : données statiques
  - Table F : données dynamiques

### Règlement UE 2023/1804

La règlementation en vigueur (UE 2023/1804) précise (en complément des articles liés 3 et 4 liés aux objectifs d'aménagement et abordés fin 2024) à l'article 20 les points liés aux données :

- identifiants unique délivré par l'IDRO pour les exploitants des points de recharge et les prestataires de service le 14 avril 2025,
- disponibilité sans frais des données statiques et dynamiques au 14 avril 2025,
- Au plus tard le 31 décembre 2024, accessibilité sur une base ouverte et non discriminatoire à tous les utilisateurs des données statiques et dynamiques par l’intermédiaire de leur point d’accès national,
- données statiques :
  - localisation géographique des points de recharge,
  - nombre de connecteurs,
  - nombre de places réservées aux personnes handicapées,
  - les coordonnées du propriétaire et de l’exploitant de la station de recharge,
  - les horaires d’ouverture,
  - les codes ID, au moins de l’exploitant du point de recharge,
  - le type de connecteur,
  - le type de courant (AC/DC),
  - la puissance de sortie maximale (kW) de la station de recharge,
  - la puissance de sortie maximale (kW) du point de recharge,
  - la compatibilité avec les types de véhicules,
- données dynamiques (données variables non nécessairement liées aux session/status ex. prix ad-hoc):
  - le statut opérationnel (opérationnel/hors service),
  - la disponibilité (en cours d’utilisation/libre),
  - le prix ad-hoc (tarification applicable pour une charge unique),
  - le caractère 100 % renouvelable de l’électricité fournie (oui/non),

### projet de modification de fin 2024

Le projet mis en relecture fin 2024 propose les modifications suivantes :

- remplacement de la "localisation géographique des points de recharge" par les attributs suivants :
  - global navigation satellite system (GNSS) geographic location information (latitude/ longitude WGS84),
  - additional geographic location information (ex. niveau d'un parking),
  - country,
  - region,
  - city or town,
  - postal code,
  - address name,
- remplacement des "coordonnées du propriétaire et de l’exploitant de la station de recharge" par :
  - Legal name of the recharging point operator or owner,
  - Commercial name of the recharging point operator or owner,
  - Service support (A4). Présence personne à la station,
  - Helpdesk telephone (A5). Voir format défini dans la spécification,
- abandon du code ID de l'exploitant du point de recharge,
- remplacement de "horaires d’ouverture" par :
  - Opening time,
  - Time zone,
- le caractère renouvelable de l'énergie est déplacé de données dynamiques à données statiques,
- ajout des données statiques suivantes :
  - Number of recharging points,
  - Facilities offering associated services to the user (services proches de la station),
  - Vehicle specifications permitted,
  - Number of parking spaces,
  - Payment device with bank card reader,
  - Payment device with a contactless functionality that is at least able to read payment cards,
  - Other ad hoc payment option,
  - Additional information about payment providers accepted,
  - Contract-based (subscription) payment option,
  - Recharging point ID code (connector),
  - Mobility service providers offering contract-based recharging,
  - Plug-and-charge,
  - Smart recharging services,

### Impacts sur le modèle de données Qualicharge

Une prise en compte des données AFIR, sans analyse détaillée des attributs, aurait les impacts suivants dans le modèle des données Qualicharge :

- modèle de données :
  - pas de remise en cause des entités actuelle (la notion de connecteur n'est pas nécessaire, la notion de propriétaire est peut-être à revoir en fonction des entités aménageur/enseigne),
  - ajout éventuel de la notion de pool (ou de station de station) pour gérer les données liées aux articles 3 et 4,
  - formats à revoir en fonction de la spécification,
  - déplacement de certains attributs entre station et point de recharge (la station devient l'entité de gestion et le point de recharge l'entité technique)

- entité localisation :
  - les attributs définis (A9, A10, A11) sont déjà présents via les tables liées,
  - le code postal (A12) peut se déduire du code INSEE,
  - ajout éventuel de "additional geographic location information" (A8)

- entité point de recharge
  - ajout du nombre de connecteurs (B2)
  - ajout du type de courant (AC/DC) (B4)
  - ajustement de restriction_gabarit par Vehicle_specifications_permitted (A17). A remonter au niveau de la station ?
  - ajout du type de connecteurs MCS (B3)
  - tarification à remonter au niveau de la station ?
  - ajout de Plug-and-charge (B8),
  - ajout de Smart recharging services (B9)

- entité station
  - ajout du service support (A4). Ou bien attribut mis en commun au niveau de l'entité opérateur.
  - ajout du nombre de places (A18)
  - ajout du nombre de places handicapées (A19)
  - horaires à remplacer par un format plus structuré (Opening time (A14) + Time zone (A15) ?)
  - remplacement de station_deux_roues par vehicle_type_compatibility (A16) plus générale (codification UNECE qui inclut les PL)
  - refonte de la tarification (ajout de la tarification ad-hoc (F3, A23), par contrat (A24) et du paiement sans contact (A21)),
  - ajout de la puissance maxi (B5)
  - ajout de Facilities offering associated services to the user (A6)
  - ajout de Mobility service providers offering contract-based recharging (B7),
  - ajout du caractère 100 % renouvelable de l’électricité fournie (B10) (est-ce que c'est lié au pdl ?)

- entités aménageur / enseigne (propriétaire) ?
  - distinction legal name (A1) / commercial name (A2). Mais attributs commun avec l'opérateur ?

- entités opérateur
  - distinction legal name (A1) / commercial name (A2). Mais attributs commun avec l'opérateur ?
  - ajout du service support (A4) ou bien au niveau de la station

- entité status/session
  - notion de réservation à clarifier (F2)

## Compatibilité avec les données `transport.gouv`

Pour la partie statique, les attributs du modèle de données sont identiques à ceux du dataset `transport.gouv`.
Les deux structures comportent néanmoins les écarts suivants :

- modèle de données:

    Pour QualiCharge, l'intégrité du modèle de données est garantie par la structure de la base de données et les API associés.
    Pour `transport.gouv`, l'intégrité du modèle n'est pas controlée en amont (elle l'est uniquement a posteriori).

- valeurs des attributs:

    Le niveau de qualité des attributs est contrôlé dans les deux cas en amont (via les API pour QualiCharge, via Validata pour `transport.gouv`).
    De façon générale, la niveau de qualité attendue des valeurs des attributs pour QualiCharge est plus élevé que celui de `transport.gouv`.

    Les différences relevées sont les suivantes :

    | attribut               | Qualicharge       | Schema statique |
    | :--------------------- | ----------------- | --------------- |
    | contact_amenageur      | EmailStr          | format email    |
    | contact_operateur (M)  | EmailStr          | format email    |
    | telephone_operateur    | FrenchPhoneNumber | string          |
    | nbre_pdc (M)           | PositiveInt       | int             |
    | date_maj (M)           | PastDate          | date            |
    | num_pdl                | "^\d{14}$"        | string          |
    | date_mise_en_service   | PastDate          | date            |
    | puissance_nominale (M) | PositiveFloat     | float           |

    Qualicharge intègre également le contrôle de cohérence du prefixe AFIREV entre id-station et id_pdc.

L'échange de données entre les deux bases nécessite de mettre en place une stratégie de prise en compte de ces différences (ne concerne que le sens `transport.gouv`vers QualiCharge).

## Proposition de conversion du format CSV `transport.gouv` au format CSV Qualicharge

L'objectif est de traiter les écarts de structure identifiés ci-dessus et d'éliminer les données erronées.

Les principes retenus pour traiter les données ne respectant pas le format QualiCharge sont les suivants (pour chaque donnée provoquant une erreur):

- les données facultatives sont transformées en données vides (valeur spécifique à chaque type de donnée),
- les données obligatoires dont les formats sont différentes sont transformées en données spécifiques:
  - date_maj: valeur de la date du jour (pour les date postérieures à la date du jour),
  - puissance_nominale: valeur opposée (pour les valeurs négatives)
  - nbre_pdc: valeur nulle (la valeur du champ peut être recalculée si besoin)
  - contact_operateur: à préciser (en fonction des différences entre les formats `EmailStr` et `format email`)
- les autres données obligatoires dont les formats sont identiques sont traitées comme une erreur portant sur la station (la station n'est pas prise en compte).

Le principe d'implémentation est de tester la création d'une instance de la classe `Statique` pour chaque ligne, et en cas d'erreur d'appliquer les principes ci-dessus (remplacement des données avec des formats différents et suppression des stations erronées).
