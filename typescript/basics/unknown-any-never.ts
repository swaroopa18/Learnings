let unknownVariable: unknown;
let aVariable: string;
let anyVariable: any;

unknownVariable = "variable value";
anyVariable = "any variable";
aVariable = anyVariable;
if (typeof unknownVariable == "string") aVariable = unknownVariable;

function generateError(msg: string, code: number): never {
  throw { message: msg, errorCode: code };
}

generateError("Error", 204);
