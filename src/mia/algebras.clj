(ns mia.algebras
  (:require [mia.core :as core]
            [mia.inference :as inf]))

;; === ALGEBRA DI COMPOSIZIONE ===
(defn compose-atoms [atoms]
  "Compone atomi in una molecola se possibile"
  (let [formula (inf/deduce-molecule atoms)]
    (when (not= formula "UNKNOWN")
      (let [bonds (for [i (range (dec (count atoms)))]
                    (core/create-bond (nth atoms i) (nth atoms (inc i)) :covalent))]
        (core/create-molecule atoms bonds formula)))))

(defn decompose-molecule [molecule atom-db]
  "Decompone una molecola nei suoi atomi costituenti"
  (map #(get atom-db %) (:atoms molecule)))

;; === ALGEBRA DI TRASFORMAZIONE ===
(defn balance-equation [reactants products]
  "Auto-bilancia un'equazione chimica simbolicamente"
  (let [reactant-elements (frequencies (mapcat :elements reactants))
        product-elements (frequencies (mapcat :elements products))]
    {:balanced? (= reactant-elements product-elements)
     :reactant-elements reactant-elements
     :product-elements product-elements}))

(defn react [reactant-molecules conditions]
  "Esegue una reazione simbolica tra molecole"
  (let [all-atoms (mapcat #(decompose-molecule % {}) reactant-molecules)
        shuffled-atoms (shuffle all-atoms)
        products (partition-by identity shuffled-atoms)]
    (map compose-atoms products)))

;; === ALGEBRA DI CAMPO ===
(defn field-effect [source target]
  "Calcola l'effetto di campo tra due entità"
  (let [source-charge (if (= (:element source) :hydrogen) 1 
                         (- (:protons source) (:electrons source)))
        target-charge (if (= (:element target) :hydrogen) 1 
                         (- (:protons target) (:electrons target)))]
    (cond
      (and (pos? source-charge) (neg? target-charge)) :attractive
      (and (neg? source-charge) (pos? target-charge)) :attractive
      (and (pos? source-charge) (pos? target-charge)) :repulsive
      (and (neg? source-charge) (neg? target-charge)) :repulsive
      :else :neutral)))

(defn superposition [fields]
  "Combina multipli campi usando principio di sovrapposizione"
  (reduce (fn [acc field]
            {:intensity (+ (:intensity acc 0) (:intensity field))
             :direction (if (= (:direction acc) (:direction field)) 
                           (:direction acc) :mixed)})
          {:intensity 0 :direction :null}
          fields))

;; === ALGEBRA DI STATO ===
(defn phase-transition [molecule from-phase to-phase conditions]
  "Gestisce transizioni di fase simboliche"
  (let [energy-required (case [from-phase to-phase]
                          [:solid :liquid] 100
                          [:liquid :gas] 200
                          [:solid :gas] 300
                          [:gas :liquid] -200
                          [:liquid :solid] -100
                          [:gas :solid] -300
                          0)]
    (assoc molecule :properties 
           (assoc (:properties molecule) 
                  :phase to-phase
                  :energy-delta energy-required))))