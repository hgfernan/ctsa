# Architecture of tests for the `sarima` library

The systematic use of software testing is growing stronger in the latest years, as it can improve the reliability and increase the maturity of the application it is applied to.

Since statistical applications and libraries are getting larger and more complex, they should benefit from the use of software testing.

Unfortunately, to our best knowledge, the testing support libraries are deterministic in nature, while the result of statistical sofware applications are probabilistic in nature.

That is: usually the test support libraries deal with test results that can only be false or true, while the typical statatistical results are related to probabilities.

That's an interesting problem that won't be dealt with in this text. The purpose of this text is to present two practical strategies to test ctsa,
