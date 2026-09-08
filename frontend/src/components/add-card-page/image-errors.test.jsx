import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AddCardPage } from "./add-card-page";
import { EditCardPage } from "../edit-card-page/edit-card-page";
import { getAchievements, sendCard, updateCard } from "../../utils/api";

jest.mock("../../utils/api");
beforeEach(() => { getAchievements.mockResolvedValue([]); });

test.each(["create", "edit"])("shows image API errors on %s", async (mode) => {
  sendCard.mockRejectedValue({ image: ["Invalid image."] });
  updateCard.mockRejectedValue({ image: ["Invalid image."] });
  render(<MemoryRouter>{mode === "create" ? <AddCardPage /> :
    <EditCardPage data={{ id: 1, name: "Cat", color: "white", birth_year: 2020, achievements: [] }} setData={() => {}} />
  }</MemoryRouter>);
  fireEvent.click(screen.getByText("Сохранить"));
  expect(await screen.findByRole("alert")).toHaveTextContent("Invalid image.");
});

test("rejects unsupported files with a visible error", async () => {
  const { container } = render(<MemoryRouter><AddCardPage /></MemoryRouter>);
  fireEvent.change(container.querySelector('input[type="file"]'), {
    target: { files: [new File(["text"], "cat.txt", { type: "text/plain" })] },
  });
  fireEvent.click(screen.getByText("Сохранить"));
  expect(await screen.findByRole("alert")).toHaveTextContent("JPEG или PNG");
});
