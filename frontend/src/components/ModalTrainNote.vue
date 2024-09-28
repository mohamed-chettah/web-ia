<script setup>
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from "@headlessui/vue";
import {defineProps, defineEmits, ref} from "vue";

// Props pour contrôler l'ouverture/fermeture de la modal
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
});

async function trainNote() {
  try {
    const response = await fetch('http://localhost:5001/train-note', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (response.ok) {
      alert('Modèle de prédiction pour les notes entraîné avec succès !');
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

const form = ref({
  ville: '',
  prix: 0,
  surface: 0,
})


const response = ref()
async function predictNote() {
  try {
    const res = await fetch('http://localhost:5001/predict-note', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form.value)
    });
    if (res.ok) {
      response.value = await res.json(); // Stocke la réponse en JSON
      console.log(response.value); // Affiche la réponse dans la console
    } else {
      alert('Modèle non entraîné pour les notes !')
    }
  } catch (error) {
    console.error('Error:', error);
  }
}


// Événements émis pour informer le parent de la fermeture de la modal
const emit = defineEmits(['close']);

// Fonction pour fermer la modal
function closeModal() {
  emit('close');
}
</script>

<template>
  <!-- TransitionRoot pour la modal -->
  <TransitionRoot :show="isOpen" appear as="template">
    <Dialog as="div" class="relative z-10" @close="closeModal">
      <div class="fixed inset-0 bg-black/30" />

      <!-- Modal Content -->
      <div class="fixed inset-0 flex items-center justify-center p-4 text-center">
        <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
        >
          <DialogPanel class="w-full max-w-md transform bg-white p-6 rounded-lg shadow-xl">
            <!-- Titre de la modal -->
            <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
              Modèle de Prédiction Notes
            </DialogTitle>

            <!-- Bouton pour fermer la modal -->
            <button @click="closeModal" class="absolute top-2 right-2 text-gray-400 hover:text-gray-600 focus:outline-none">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            <!-- Contenu de la modal -->
            <div class="mt-4">
              <p class="text-sm text-gray-500">
                Ici, vous pouvez entraîner et utiliser votre modèle de prédiction.
              </p>

              <a @click="trainNote()" class="group flex mt-5 items-center px-3 py-2 cursor-pointer text-sm font-medium text-white transition-all duration-200 bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 shadow-md hover:shadow-lg">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 mr-2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 1.5m-.5-1.5h-9.5m0 0-.5 1.5m.75-9 3-3 2.148 2.148A12.061 12.061 0 0 1 16.5 7.605" />
                </svg>
                <span class="mr-2">Entrainer le modèle de prédiction pour les notes</span>
              </a>

              <!-- Formulaire pour envoyer des données au backend -->
              <form @submit.prevent="predictNote">
                <div class="mt-4">
                  <label class="block text-sm font-medium text-gray-700">Ville</label>
                  <select v-model="form.ville" required class="block w-full mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    <option value="lyon">Lyon</option>
                    <option value="paris">Paris</option>
                    <option value="marseille">Marseille</option>
                  </select>
                </div>

                <div class="mt-4">
                  <label class="block text-sm font-medium text-gray-700">Prix</label>
                  <input v-model="form.prix" required type="number" class="block w-full mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="100 000 €">
                </div>

                <div class="mt-4">
                  <label class="block text-sm font-medium text-gray-700">Surface</label>
                  <input v-model="form.surface" required type="number" class="block w-full mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="100 m²">
                </div>

                <div class="mt-4">
                  <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                    Prédiction
                  </button>
                </div>
              </form>


              <div v-if="response">
                <p class="mt-4 text-sm text-gray-500">
                  Prédiction Notes: {{ response ? response.predicted_note : 'Aucune prédiction' }}
                </p>
              </div>
            </div>
          </DialogPanel>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<style scoped>
/* Styles optionnels supplémentaires */
</style>
