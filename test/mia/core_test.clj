(ns mia.core-test
  (:require [clojure.test :refer :all]
            [mia.core :as core]
            [mia.algebras :as alg]
            [mia.inference :as inf]))

(deftest test-atom-creation
  (testing "Basic atom creation"
    (let [h (core/create-atom :hydrogen)]
      (is (= (:element h) :hydrogen))
      (is (= (:protons h) 1))
      (is (= (:electrons h) 1))))
  
  (testing "Different elements"
    (let [c (core/create-atom :carbon)
          o (core/create-atom :oxygen)]
      (is (= (:protons c) 6))
      (is (= (:protons o) 8)))))

(deftest test-molecule-composition
  (testing "H2O formation"
    (let [h1 (core/create-atom :hydrogen)
          h2 (core/create-atom :hydrogen)
          o1 (core/create-atom :oxygen)
          h2o (alg/compose-atoms [h1 h2 o1])]
      (is (not (nil? h2o)))
      (is (= (:formula h2o) "H2O")))))