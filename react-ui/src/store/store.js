import { configureStore } from "@reduxjs/toolkit";
import { chatSlice } from "./chat-slice";

const store = configureStore({
  reducer: {
    chat: chatSlice.reducer,
  },
});

export default store;
