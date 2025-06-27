import { defineStore } from 'pinia';
import { getOwnedCds } from '@/api/ownedCds'
import { getWishedCds, deleteCollisions } from '@/api/wishedCds'

export const useDiscStore = defineStore('discs', {
  state: () => ({
    owned: [],
    wished: [],
    loading: false,
  }),
  actions: {
    async fetchDiscs() {
      this.loading = true;
      try {
        const [ownedRes, wishedRes] = await Promise.all([getOwnedCds(), getWishedCds()]);
        this.owned = ownedRes.data;
        this.wished = wishedRes.data;
      } catch (error) {
        console.error('Failed to fetch discs', error);
      } finally {
        this.loading = false;
      }
    },
    async removeCollisions() {
      try {
        await deleteCollisions();
        await this.fetchDiscs();
      } catch (error) {
        console.error('Error deleting collisions:', error);
      }
    }
  }
});

