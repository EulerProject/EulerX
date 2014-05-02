% Define the domain (universe of discourse): 1,2,...
u(1..3).
% every element is either in or out
i(X) :- u(X), not o(X).
o(X) :- u(X), not i(X).
