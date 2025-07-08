// src/store/formStore.ts
import { create } from "zustand";

type FormState = {
  isLoading: boolean;
  setLoading: (val: boolean) => void;
};

export const useFormStore = create<FormState>((set) => ({
  isLoading: false,
  setLoading: (val) => set({ isLoading: val }),
}));
