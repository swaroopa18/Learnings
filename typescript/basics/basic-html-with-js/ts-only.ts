//Addition of two numbers
const button = document.querySelector('button')! as HTMLInputElement;
const input1 = document.getElementById('num1')! as HTMLInputElement;
const input2 = document.getElementById('num2')! as HTMLInputElement;

const add = (num1: number, num2: number) => {
    return num1 + num2
}
button.addEventListener('click', function () {
    console.log("Addition is", add(+input1.value, +input2.value))
})
