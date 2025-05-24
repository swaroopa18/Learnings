let greetings: string = "Hello World";

greetings.toUpperCase();
console.log(greetings);

function add20(a: number): Promise<number> {
  return Promise.resolve(a + 20);
}

async function getFavoriteNumber(): Promise<number> {
  return 26;
}

type type1 = {
  prop: string;
};

type type2 = type1 & {
  prop: number;
};


interface Interface1 {
    prop: string;
}

interface Interface2 extends Interface1 {
    prop: string;
}


