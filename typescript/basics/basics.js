function add(n1, n2, showResult, phrase) {
    var result = n1 + n2;
    if (showResult) {
        console.log(phrase + result);
    }
    return result;
}
var num1 = 6;
var num2 = 1.4;
var printResult = true;
var resultPhrase = "Result is ";
console.log(add(num1, num2, printResult, resultPhrase));
