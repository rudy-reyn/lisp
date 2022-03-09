# Lisp

Lisp dialect implemented in Python written by me over the past few days.

Use `python3 lisp filename` to run.

Only uses a handful of restricted keywords:
```lisp
    =>      ;; for function declaration
    let     ;; for variable definition
    if/else ;; if statements
    and/or  ;; short cuirceted and/or evaluations.
```

```lisp
;; Functions are first class, and anonymous and named functions function identically.
(let fact (=> n a               ; function signature
    (if (<= n 0) a              ; first paraentheses indicate start of block
        (fact (- n 1) (* n a))
        )))

;; Higher order and recursive functions are also easy to implement.

(let quicksort (=> arr
    (if (empty? arr)                ; if statements are terminated by blocks, so else is optional.
        arr
    (let pivot (head arr))
    (let lo (filter (tail arr) (=> i (<  i pivot))))
    (let hi (filter (tail arr) (=> i (>= i pivot))))
    (++ (+ (quicksort lo) pivot)            ; + used to append identifier to end of array
           (quicksort hi)))))               ; ++ used to concat arrays

(let adder (=> n (=> m (+ n m))))   ; Returns a new function
(let add2 (adder 2))
(print (add2 3))    ;; prints 5
```
