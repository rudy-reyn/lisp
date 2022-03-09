;; 03/02/2022
;; example.lisp

(let even? (=> n (== (% n 2) 0)))
(let le0? (=> n (<= n 0)))
(let sqrt (=> n (** n (/ 1 2))))

(let addr (=> x (=> y (+ x y))))
(let ++10 (addr 10))

(let fibonacci (=> n (
     (if (< n 2) n
         (+ (fibonacci (- n 1))
            (fibonacci (- n 2)))))))

(let ! (=> n
     (if (le0? n) 1
         (* n (! (- n 1))))))

(print (fibonacci 10))
(print (! 10))
(print (sqrt 2)) (print (sqrt 9))
