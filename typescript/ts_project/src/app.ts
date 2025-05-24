class Input {
  template: HTMLTemplateElement;
  root: HTMLDivElement;
  element: HTMLFormElement;
  constructor() {
    this.root = document.getElementById("app")! as HTMLDivElement;
    this.template = document.getElementById(
      "project-input"
    )! as HTMLTemplateElement;

    const importedNode = document.importNode(this.template.content, true);
    this.element = importedNode.firstElementChild as HTMLFormElement;
    this.attach();
  }
  private attach() {
    const a= new TypeError('')

    this.root.insertAdjacentElement("afterbegin", this.element);
  }
}

new Input();
