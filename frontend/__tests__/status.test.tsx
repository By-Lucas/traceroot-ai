import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Status } from "@/components/status";
describe("Status", () => {
  it("renders readable verification state", () => {
    render(<Status value="PARTIALLY_VERIFIED" />);
    expect(screen.getByText("PARTIALLY VERIFIED")).toBeInTheDocument();
  });
});
