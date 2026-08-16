import { twMerge } from "tailwind-merge";

type ClassValue = string | undefined | null | false;

export function cn(...inputs: ClassValue[]) {
  return twMerge(
    inputs.filter((x): x is string => typeof x === "string").join(" ")
  );
}
