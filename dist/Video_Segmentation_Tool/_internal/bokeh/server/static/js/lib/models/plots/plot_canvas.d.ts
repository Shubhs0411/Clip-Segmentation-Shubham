import { CartesianFrame } from "../canvas/cartesian_frame";
import type { CanvasView, FrameBox } from "../canvas/canvas";
import type { Renderer, RendererView } from "../renderers/renderer";
import type { DataRenderer } from "../renderers/data_renderer";
import type { Range } from "../ranges/range";
import type { Tool } from "../tools/tool";
import type { Selection } from "../selections/selection";
import type { LayoutDOM, DOMBoxSizing, FullDisplay } from "../layouts/layout_dom";
import { LayoutDOMView } from "../layouts/layout_dom";
import type { Plot } from "./plot";
import { Title } from "../annotations/title";
import { AxisView } from "../axes/axis";
import type { ToolbarPanelView } from "../annotations/toolbar_panel";
import { ToolbarPanel } from "../annotations/toolbar_panel";
import type { AutoRanged } from "../ranges/data_range1d";
import type { ViewStorage, IterViews } from "../../core/build_views";
import type { Renderable } from "../../core/visuals";
import type { RenderLevel } from "../../core/enums";
import type { SerializableState } from "../../core/view";
import { Signal0 } from "../../core/signaling";
import type { Context2d } from "../../core/util/canvas";
import { CanvasLayer } from "../../core/util/canvas";
import type { Layoutable } from "../../core/layout";
import { BorderLayout } from "../../core/layout/border";
import { BBox } from "../../core/util/bbox";
import type { RangeInfo, RangeOptions } from "./range_manager";
import { RangeManager } from "./range_manager";
import type { StateInfo } from "./state_manager";
import { StateManager } from "./state_manager";
import type { StyleSheetLike } from "../../core/dom";
import { InlineStyleSheet } from "../../core/dom";
export declare class PlotView extends LayoutDOMView implements Renderable {
    model: Plot;
    visuals: Plot.Visuals;
    layout: BorderLayout;
    frame: CartesianFrame;
    private _render_count;
    canvas_view: CanvasView;
    get canvas(): CanvasView;
    readonly repainted: Signal0<this>;
    protected _computed_style: InlineStyleSheet;
    stylesheets(): StyleSheetLike[];
    protected _title?: Title;
    protected _toolbar?: ToolbarPanel;
    get toolbar_panel(): ToolbarPanelView | undefined;
    protected _outer_bbox: BBox;
    protected _inner_bbox: BBox;
    protected _needs_paint: boolean;
    protected _invalidated_painters: Set<RendererView>;
    protected _invalidate_all: boolean;
    protected _state_manager: StateManager;
    protected _range_manager: RangeManager;
    get state(): StateManager;
    set invalidate_dataranges(value: boolean);
    protected _is_paused?: number;
    protected lod_started: boolean;
    protected _initial_state: StateInfo;
    protected throttled_paint: () => void;
    computed_renderers: Renderer[];
    get computed_renderer_views(): RendererView[];
    renderer_view<T extends Renderer>(renderer: T): T["__view_type__"] | undefined;
    get auto_ranged_renderers(): (RendererView & AutoRanged)[];
    get base_font_size(): number | null;
    readonly renderer_views: ViewStorage<Renderer>;
    readonly tool_views: ViewStorage<Tool>;
    children(): IterViews;
    get is_paused(): boolean;
    get child_models(): LayoutDOM[];
    pause(): void;
    unpause(no_render?: boolean): void;
    private _needs_notify;
    notify_finished_after_paint(): void;
    request_render(): void;
    request_paint(to_invalidate: RendererView[] | RendererView | "everything"): void;
    invalidate_painters(to_invalidate: RendererView[] | RendererView | "everything"): void;
    schedule_paint(): void;
    request_layout(): void;
    reset(): void;
    remove(): void;
    render(): void;
    initialize(): void;
    lazy_initialize(): Promise<void>;
    box_sizing(): DOMBoxSizing;
    protected _intrinsic_display(): FullDisplay;
    _update_layout(): void;
    protected _measure_layout(): void;
    get axis_views(): AxisView[];
    update_range(range_info: RangeInfo, options?: RangeOptions): void;
    reset_range(): void;
    trigger_ranges_update_event(extra_ranges?: Range[]): void;
    get_selection(): Map<DataRenderer, Selection>;
    update_selection(selections: Map<DataRenderer, Selection> | null): void;
    reset_selection(): void;
    protected _invalidate_layout_if_needed(): void;
    get_renderer_views(): RendererView[];
    protected _compute_renderers(): Generator<Renderer, void, undefined>;
    build_renderer_views(): Promise<void>;
    build_tool_views(): Promise<void>;
    connect_signals(): void;
    has_finished(): boolean;
    _after_layout(): void;
    repaint(): void;
    paint(): void;
    protected _actual_paint(): void;
    protected _paint_levels(ctx: Context2d, level: RenderLevel, clip_region: FrameBox, global_clip: boolean): void;
    paint_layout(ctx: Context2d, layout: Layoutable): void;
    protected _paint_empty(ctx: Context2d, frame_box: FrameBox): void;
    protected _paint_outline(ctx: Context2d, frame_box: FrameBox): void;
    export(type?: "auto" | "png" | "svg", hidpi?: boolean): CanvasLayer;
    serializable_state(): SerializableState;
    protected _hold_render_changed(): void;
}
//# sourceMappingURL=plot_canvas.d.ts.map