import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AuthForm } from "@/components/auth-form";
vi.mock("next/navigation", () => ({ useRouter: () => ({ push: vi.fn() }) }));
describe("AuthForm", () => {
  it("exposes accessible registration fields", () => {
    render(<AuthForm mode="register" />);
    expect(screen.getByLabelText("Display name")).toBeRequired();
    expect(screen.getByLabelText("Email")).toHaveAttribute("type", "email");
    expect(
      screen.getByRole("button", { name: /create account/i }),
    ).toBeEnabled();
  });
});
