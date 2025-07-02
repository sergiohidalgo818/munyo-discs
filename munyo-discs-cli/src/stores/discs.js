import { defineStore } from "pinia";
import { getOwnedCds } from "@/api/ownedCds";
import { deleteCollisions, getWishedCds } from "@/api/wishedCds";

export const useDiscStore = defineStore("discs", {
  state: () => ({
    owned: [],
    wished: [],
  }),
  actions: {
    async fetchDiscs() {
      const [ownedRes, wishedRes] = await Promise.all([
        getOwnedCds(),
        getWishedCds(),
      ]);
      this.owned = ownedRes.data || [];
      this.wished = wishedRes.data || [];
    },
    async removeCollisions() {
      try {
        await deleteCollisions();
        await this.fetchDiscs();
      } catch (error) {
        console.error("Error deleting collisions:", error);
      }
    },
  },
});
